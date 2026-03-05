import cadquery as cq

# Parameters
width = 200.0
length = 150.0
thickness = 2.0
corner_radius = 5.0

hole_width = 30.0
hole_length = 15.0
hole_offset_x = 0.0 # centered along width? No, it looks like it's offset.
# Let's say it's on the top edge, slightly offset to the left from center.
# Actually, looking at the image, it's on the longer edge (width), offset from the corner.
hole_pos_x = -width/2 + 30 + hole_width/2
hole_pos_y = length/2 - 10 - hole_length/2

# Create base plate
result = (
    cq.Workplane("XY")
    .box(width, length, thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Add rectangular hole with filleted corners
hole = (
    cq.Workplane("XY")
    .center(hole_pos_x, hole_pos_y)
    .box(hole_width, hole_length, thickness + 2)
    .edges("|Z")
    .fillet(2.0)
)

result = result.cut(hole)