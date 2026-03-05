import cadquery as cq

# Define dimensions
length = 50
width = 10
height = 5
hole_diameter = 5
slot_length = 30
slot_width = 5
triangle_height = 10

# Create main rectangular body
result = (
    cq.Workplane("XY")
    .box(length, width, height)
)

# Create hole
result = (
    result.faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .center(length/4, 0)
    .hole(hole_diameter)
)

# Create slot
result = (
    result.faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .center(-length/4, 0)
    .slot2D(slot_length, slot_width)
    .cutThruAll()
)

# Create triangular cut
result = (
    result.faces("<Y")
    .workplane(centerOption="CenterOfBoundBox")
    .moveTo(0, -triangle_height)
    .lineTo(length/2, 0)
    .lineTo(-length/2, 0)
    .close()
    .cutBlind(-height)
)