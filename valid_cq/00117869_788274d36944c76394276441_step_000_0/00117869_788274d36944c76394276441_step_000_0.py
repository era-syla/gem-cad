import cadquery as cq
from math import sin, cos, radians

# --- Parametric Dimensions ---
base_width = 90.0
base_height = 70.0
shaft_diameter = 26.0
shaft_length = 420.0
handle_length = 135.0
handle_tilt_angle = 12.0  # Degrees
handle_thickness = 34.0   # Major axis of grip ellipse
handle_width = 30.0       # Minor axis of grip ellipse
fillet_radius = 2.0

# --- 1. Base Construction ---
# Loft from a rounded square at the bottom to a circle at the top
# Sketch 1: Bottom Rectangle with rounded corners
s1 = (
    cq.Sketch()
    .rect(base_width, base_width)
    .vertices()
    .fillet(12.0)
)

# Sketch 2: Top Circle (matches shaft)
s2 = (
    cq.Sketch()
    .circle(shaft_diameter / 2.0)
)

# Create the Loft
base = (
    cq.Workplane("XY")
    .placeSketch(s1)
    .add(
        cq.Workplane("XY")
        .workplane(offset=base_height)
        .placeSketch(s2)
    )
    .loft(combine=True)
)

# --- 2. Shaft Construction ---
# Extrude the shaft from the top face of the base
shaft = (
    base.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# --- 3. Handle Construction ---
# The handle sits at the top of the shaft and tilts slightly
shaft_top_z = base_height + shaft_length
start_point = cq.Vector(0, 0, shaft_top_z)

# Calculate tilt direction vector (tilting in -X direction)
angle_rad = radians(handle_tilt_angle)
handle_dir = cq.Vector(-sin(angle_rad), 0, cos(angle_rad))

# Helper to create workplanes along the handle axis
def get_handle_plane(dist):
    center = start_point + handle_dir * dist
    # Orient plane with normal along handle_dir. 
    # xDir=(0,1,0) aligns the local X with global Y for the ellipse orientation.
    return cq.Workplane(cq.Plane(origin=center, xDir=cq.Vector(0, 1, 0), normal=handle_dir))

# Profile 1: Interface with shaft (Circle)
prof1 = get_handle_plane(0).circle(shaft_diameter / 2.0)

# Profile 2: Lower grip section (Ellipse)
prof2 = get_handle_plane(handle_length * 0.3).ellipse(handle_width/2.0, handle_thickness/2.0)

# Profile 3: Upper grip section (Ellipse)
prof3 = get_handle_plane(handle_length * 0.9).ellipse(handle_width/2.0, handle_thickness/2.0)

# Generate Handle Body via Loft
handle_body = (
    cq.Workplane("XY") # Container
    .add(prof1.wire())
    .add(prof2.wire())
    .add(prof3.wire())
    .toPending()
    .loft()
)

# Handle Cap
handle_cap = (
    get_handle_plane(handle_length * 0.9)
    .ellipse(handle_width/2.0, handle_thickness/2.0)
    .extrude(8.0)
    .edges(">Z")
    .fillet(3.0)
)

# Combine main structures
structure = shaft.union(handle_body).union(handle_cap)

# --- 4. Finger Grooves ---
# Cut grooves into the "front" (relative to tilt) side of the handle
groove_radius = 8.5
groove_depth_cut = 3.0
num_grooves = 4
groove_start_dist = 30.0
groove_spacing = 24.0

# Normal vector perpendicular to handle axis in XZ plane (pointing towards +X side)
# This determines which side of the handle we cut
handle_normal = cq.Vector(cos(angle_rad), 0, sin(angle_rad))

cutters = cq.Workplane("XY")

for i in range(num_grooves):
    dist = groove_start_dist + i * groove_spacing
    pos_on_axis = start_point + handle_dir * dist
    
    # Calculate cutter center to achieve desired cut depth
    # Move radially outward from axis
    offset = (handle_thickness / 2.0) + groove_radius - groove_depth_cut
    cutter_center = pos_on_axis + handle_normal * offset
    
    # Create cylindrical cutter oriented horizontally (Global Y axis)
    cutter = (
        cq.Workplane(cq.Plane(origin=cutter_center, xDir=cq.Vector(1,0,0), normal=cq.Vector(0,1,0)))
        .circle(groove_radius)
        .extrude(handle_width * 2, both=True)
    )
    cutters = cutters.add(cutter)

# Apply cuts
result = structure.cut(cutters)

# Final cleanup: Fillet the bottom edges of the base
result = result.edges("<Z").fillet(fillet_radius)