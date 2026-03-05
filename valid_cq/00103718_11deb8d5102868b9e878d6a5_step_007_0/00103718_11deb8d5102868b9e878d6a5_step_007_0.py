import cadquery as cq

# Model parameters
head_width = 20.0
head_depth = 12.0
head_height = 30.0

shaft_width = 8.0
shaft_depth = 8.0
shaft_length = 50.0

# Create the geometry
# 1. Start with the top block (head), centered on the XY plane
# 2. Select the bottom face of the head
# 3. Sketch the shaft profile and extrude downwards
result = (
    cq.Workplane("XY")
    .box(head_width, head_depth, head_height)
    .faces("<Z")
    .workplane()
    .rect(shaft_width, shaft_depth)
    .extrude(shaft_length)
)