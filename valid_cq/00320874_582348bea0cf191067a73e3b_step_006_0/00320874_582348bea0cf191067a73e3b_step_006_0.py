import cadquery as cq

# --- Dimensions ---
handle_length = 95.0
handle_max_radius = 16.0
handle_back_radius = 6.0
handle_neck_radius = 7.0
collar_radius = 9.0
collar_length = 10.0

shaft_diameter = 6.0
shaft_length = 130.0

tip_length = 10.0
tip_width = 7.0
tip_thickness = 1.2

groove_count = 6
groove_depth = 2.0

# --- 1. Handle Construction ---

# Define the profile for the revolved handle
# Origin (0,0,0) is at the back center of the handle
p_start = (0, 0)
p_back_arc_end = (5, handle_back_radius)
p_belly = (45, handle_max_radius)
p_taper = (handle_length - collar_length - 5, handle_neck_radius)
p_collar_start = (handle_length - collar_length, collar_radius)
p_collar_end = (handle_length, collar_radius)
p_axis_end = (handle_length, 0)

# Create the main handle body
handle_profile = (
    cq.Workplane("XY")
    .moveTo(*p_start)
    # Back dome approximation
    .lineTo(0, 4) 
    .spline([p_back_arc_end], includeCurrent=True)
    # Main body bulge
    .spline([p_belly, p_taper], includeCurrent=True)
    # Collar transition
    .lineTo(*p_collar_start)
    .lineTo(*p_collar_end)
    .lineTo(*p_axis_end)
    .close()
)

handle = handle_profile.revolve(360, (0,0,0), (1,0,0))

# --- 2. Grip Grooves ---

# We create a "cutter" tool to subtract material.
# The cutter is created by sweeping a circle along a curved path.
# The path is positioned so the cutter intersects the handle surface.

# Path definition: roughly parallel to handle profile but offset
# Coordinates chosen to ensure groove tapers off at ends
path_pts = [
    (15, handle_back_radius + 6),  # Start high (shallow/no cut)
    (45, handle_max_radius + 4),   # Middle (deepest cut relative to surface)
    (75, handle_neck_radius + 5)   # End high
]

cutter_path_wire = (
    cq.Workplane("XY")
    .moveTo(path_pts[0][0], path_pts[0][1])
    .threePointArc(path_pts[1], path_pts[2])
)

# Profile definition: A circle perpendicular to the start of the path
# A large radius creates a wider, shallower looking groove
cutter_radius = 6.0

cutter_profile = (
    cq.Workplane("YZ")
    .workplane(offset=path_pts[0][0])
    .moveTo(path_pts[0][1], 0)
    .circle(cutter_radius)
)

# Create the single cutter solid
cutter_solid = cutter_profile.sweep(cutter_path_wire)

# Subtract cutters in a radial pattern
for i in range(groove_count):
    angle = i * (360.0 / groove_count)
    # Rotate the cutter around the handle axis (X)
    rotated_cutter = cutter_solid.rotate((0,0,0), (1,0,0), angle)
    handle = handle.cut(rotated_cutter)

# Add a small fillet to the back edge for comfort
try:
    handle = handle.edges("<X").fillet(2.0)
except:
    pass

# --- 3. Shaft ---

# Extrude the shaft from the flat front face of the handle
handle_and_shaft = (
    handle.faces(">X")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# --- 4. Tip ---

# Create the flared tip using a loft.
# Loft transitions from the circular shaft cross-section to a rectangular blade.

# Get the end position of the shaft
total_current_length = handle_length + shaft_length

# Create the tip solid separately
tip_solid = (
    cq.Workplane("YZ")
    .workplane(offset=total_current_length)
    .circle(shaft_diameter / 2.0) # Start profile matching shaft
    .workplane(offset=tip_length)
    .rect(tip_width, tip_thickness) # End profile (flat blade)
    .loft()
)

# Create the wedge cuts to sharpen the tip (optional but adds realism)
# We define a cutting tool to taper the thickness at the very end
wedge_cut_plane = (
    cq.Workplane("XY")
    .workplane(offset=total_current_length + tip_length/2)
)

# Combine all parts
result = handle_and_shaft.union(tip_solid)

# Add a small chamfer to the tip edge
try:
    result = result.edges(">X").chamfer(0.2)
except:
    pass

# Export or display is handled by the environment, 'result' is the final variable