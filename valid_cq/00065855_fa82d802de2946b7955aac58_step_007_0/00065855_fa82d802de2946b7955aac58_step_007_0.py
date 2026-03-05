import cadquery as cq

# Dimensions
plate_width = 100.0
plate_depth = 70.0
plate_thickness = 10.0
slot_width = 40.0
slot_depth = 40.0
vertical_corner_radius = 6.0
edge_fillet_radius = 2.0

# 1. Create the main base plate
# Centered at origin (0,0,0)
result = cq.Workplane("XY").box(plate_width, plate_depth, plate_thickness)

# 2. Create the U-shaped slot
# Select the "back" face (positive Y), draw the slot profile, and cut into the solid
result = (
    result
    .faces(">Y")             # Select the face at Y = plate_depth/2
    .workplane()             # Initialize workplane on that face
    .rect(slot_width, plate_thickness) # Draw rectangle for the slot width and full thickness
    .cutBlind(-slot_depth)   # Cut inwards (negative direction) by slot_depth
)

# 3. Fillet the vertical edges
# Select all edges parallel to the Z axis (includes outer corners and inner slot corners)
result = result.edges("|Z").fillet(vertical_corner_radius)

# 4. Fillet the top and bottom edges
# Select all edges perpendicular to the Z axis
result = result.edges("#Z").fillet(edge_fillet_radius)