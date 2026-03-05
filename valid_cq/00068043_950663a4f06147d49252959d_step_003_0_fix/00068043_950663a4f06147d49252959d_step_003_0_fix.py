import cadquery as cq

# Parameters
length = 200.0
width = 20.0
height = 20.0
slot_width = 6.0
slot_depth = 8.0
hole_diameter = 5.0
hole_offset = 25.0

# Create base bar
result = cq.Workplane("XY").box(length, width, height)

# Cut the long rectangular slot on the top face
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(length, slot_width)
    .cutBlind(slot_depth)
)

# Drill two holes in the front face
hole_positions = [
    (-length/2 + hole_offset, 0),
    ( length/2 - hole_offset, 0),
]
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)