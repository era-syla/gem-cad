import cadquery as cq

# Main block dimensions
length = 80
width = 35
height = 40

# Create the main rectangular block
result = cq.Workplane("XY").box(length, width, height)

# Add a slot/groove on the left face (the stepped feature visible on the left side)
# The left side has a stepped profile - cut a groove along the left face
result = (result
    .faces("<X")
    .workplane()
    .center(0, 0)
    .rect(width * 0.6, height * 0.3)
    .cutBlind(-8)
)

# Add a U-shaped notch on the top face toward one end
notch_width = 12
notch_depth = 8
notch_length = 10

result = (result
    .faces(">Z")
    .workplane()
    .center(15, 0)
    .rect(notch_width, notch_depth)
    .cutBlind(-10)
)

# Apply chamfers to the left face edges to create the stepped appearance
result = (result
    .faces("<X")
    .edges()
    .chamfer(3)
)

result