import cadquery as cq

# Parameters for the aluminum extrusion profile
width = 20.0
length = 400.0
slot_width = 6.0
slot_depth = 6.0
hole_diameter = 5.0
corner_radius = 1.5

# Create the base rectangular block and round the long outer edges
result = cq.Workplane("XY").box(width, width, length)
result = result.edges("|Z").fillet(corner_radius)

# Create cutting tools for the 4 side slots
# Box depth is doubled (slot_depth*2) to overlap the outer edge properly, 
# and length is increased to ensure clean cuts completely through.
slot_tool_top = cq.Workplane("XY").center(0, width/2).box(slot_width, slot_depth*2, length + 2)
slot_tool_bottom = cq.Workplane("XY").center(0, -width/2).box(slot_width, slot_depth*2, length + 2)
slot_tool_right = cq.Workplane("XY").center(width/2, 0).box(slot_depth*2, slot_width, length + 2)
slot_tool_left = cq.Workplane("XY").center(-width/2, 0).box(slot_depth*2, slot_width, length + 2)

# Subtract the slots from the base profile
result = (
    result
    .cut(slot_tool_top)
    .cut(slot_tool_bottom)
    .cut(slot_tool_right)
    .cut(slot_tool_left)
)

# Cut the central through-hole
result = result.faces(">Z").workplane().circle(hole_diameter / 2.0).cutThruAll()