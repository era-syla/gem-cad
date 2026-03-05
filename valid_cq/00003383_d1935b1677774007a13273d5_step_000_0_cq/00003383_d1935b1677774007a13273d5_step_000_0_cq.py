import cadquery as cq

# --- Parameters ---
wheel_diameter = 100.0
rim_thickness = 5.0  # Thickness of the outer ring radially
wheel_width = 10.0   # Thickness of the wheel (depth)

hub_diameter = 15.0
hub_length = 15.0    # Hub sticks out a bit more than the rim
bore_diameter = 5.0  # Central hole

num_spokes = 5
spoke_width_inner = 8.0 # Width near hub
spoke_width_outer = 4.0 # Width near rim

fillet_radius = 2.0

# --- Geometry Construction ---

# 1. Create the outer Rim
# We create a cylinder and cut out the center to make a ring
rim = cq.Workplane("XY").circle(wheel_diameter / 2.0).extrude(wheel_width)
rim_inner_cutout = cq.Workplane("XY").circle((wheel_diameter / 2.0) - rim_thickness).extrude(wheel_width)
rim = rim.cut(rim_inner_cutout)

# 2. Create the Hub
# The hub is often slightly thicker/longer than the rim to act as a spacer
hub = cq.Workplane("XY").circle(hub_diameter / 2.0).extrude(hub_length)
# Center the hub relative to the rim width (centering Z)
hub = hub.translate((0, 0, (wheel_width - hub_length) / 2.0))

# 3. Create Spokes
# We'll create one spoke and pattern it.
# A spoke connects the hub to the rim. 
# We'll sketch a profile on the XY plane and extrude it.

# Calculate spoke length to ensure overlap for union
spoke_len = (wheel_diameter / 2.0) - rim_thickness/2.0
spoke_start_offset = (hub_diameter/2.0) * 0.5 # Start slightly inside hub

# Define a single spoke profile
# We use a loft or a tapered extrude, but a sketch with arcs looks more like the organic shape in the image.
# The image shows spokes that are wider at the hub and narrower at the rim, with curved sides.

def create_spoke_shape(width_inner, width_outer, length, thickness):
    # Points for a trapezoidal/curved spoke
    # We will orient it along the Y axis for easier rotation later
    
    pts = [
        (-width_inner/2.0, spoke_start_offset), # Bottom Left
        (width_inner/2.0, spoke_start_offset),  # Bottom Right
        (width_outer/2.0, length),             # Top Right
        (-width_outer/2.0, length)             # Top Left
    ]
    
    # Simple trapezoid extrusion
    # For more curvature (like the image), we could use splines, but a linear taper is robust.
    # Let's add a slight waist or curve by using a spline or simplified polyline.
    # Given constraints, a simple loft/taper is safer. 
    
    spoke = (cq.Workplane("XY")
             .moveTo(pts[0][0], pts[0][1])
             .lineTo(pts[1][0], pts[1][1])
             .lineTo(pts[2][0], pts[2][1])
             .lineTo(pts[3][0], pts[3][1])
             .close()
             .extrude(thickness)
             )
    return spoke

# Create one spoke
single_spoke = create_spoke_shape(spoke_width_inner, spoke_width_outer, spoke_len, wheel_width)

# Pattern the spokes
spokes = single_spoke.rotate((0,0,0), (0,0,1), 360/num_spokes) # Initialize with rotation for pattern loop
all_spokes = single_spoke

for i in range(1, num_spokes):
    all_spokes = all_spokes.union(single_spoke.rotate((0,0,0), (0,0,1), i * (360.0/num_spokes)))

# 4. Combine Everything
wheel = rim.union(hub).union(all_spokes)

# 5. Create the Bore (Central Hole)
wheel = wheel.faces(">Z").workplane().circle(bore_diameter / 2.0).cutThruAll()

# 6. Add Groove to the Rim (Optional but present in pulley images)
# The image shows a slight groove or chamfer on the outer rim.
# We'll cut a V-groove into the outer face.
groove_depth = 1.0
groove_width = 3.0

path = cq.Workplane("XZ").circle(wheel_diameter/2.0)
# Profile for the cut: a triangle centered on the rim height
# Z=0 is bottom of rim, Z=wheel_width is top. Center is wheel_width/2
groove_profile = (cq.Workplane("XZ")
                  .workplane(offset=wheel_diameter/2.0) # Move to outer radius
                  .moveTo(0, wheel_width/2.0)
                  .lineTo(-groove_depth, wheel_width/2.0 - groove_width/2.0)
                  .lineTo(-groove_depth, wheel_width/2.0 + groove_width/2.0)
                  .close()
                  )
# Revolve cut is tricky with complex setups, let's use a simple geometric cut
# Construct a torus-like cutter
groove_cutter = (cq.Workplane("XZ")
                 .moveTo(wheel_diameter/2.0 + 1.0, wheel_width/2.0) # Outside
                 .lineTo(wheel_diameter/2.0 - groove_depth, wheel_width/2.0) # Tip of V
                 .lineTo(wheel_diameter/2.0 + 1.0, wheel_width/2.0 + groove_width) # Top flare
                 .lineTo(wheel_diameter/2.0 + 1.0, wheel_width/2.0 - groove_width) # Bottom flare
                 .close()
                 .revolve(360, (0,0,0), (0,0,1))
                 )

wheel = wheel.cut(groove_cutter)

# 7. Fillets
# The image shows very smooth transitions between spokes, hub, and rim.
# Filleting complex unions can be fragile in CAD kernels. We select edges carefully.

try:
    # Attempt to fillet the intersection edges between spokes and the rest
    # We select edges that are parallel to Z (the extrusion direction) and are internal
    wheel = wheel.edges("|Z").fillet(fillet_radius)
except Exception:
    # Fallback if filleting fails due to geometry complexity
    pass

result = wheel