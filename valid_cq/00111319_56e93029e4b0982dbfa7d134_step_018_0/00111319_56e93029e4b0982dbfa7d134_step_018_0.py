import cadquery as cq

# Parameters derived from visual estimation
head_diameter = 14.0
head_height = 8.0
shaft_diameter = 8.0
shaft_length = 50.0
text_content = "05-8"
text_size = 6.0
text_depth = 1.0
text_offset_x = 2.5  # Offset to create the overhang effect for the '8'

# Create the cylindrical head
# Start on XY plane, creating a cylinder for the head
result = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(head_height)

# Create the shaft
# Select the bottom face of the head (minimum Z)
# Create a workplane on that face and extrude the shaft diameter
result = (
    result.faces("<Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# Add the text "05-8" on the top face
# Select the top face (maximum Z)
# Offset the workplane center to shift the text towards the edge
# Use the text() function to create the embossed geometry
result = (
    result.faces(">Z")
    .workplane()
    .center(text_offset_x, 0)
    .text(text_content, text_size, text_depth)
)