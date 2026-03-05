import cadquery as cq

# Parameters
length = 150.0
width = 10.0
height = 10.0
hole_diameter = 5.0
end_offset = 15.0

# Build the bar
result = cq.Workplane("XY").box(length, width, height)

# Drill a hole through the top face near the left end
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-length/2 + end_offset, 0)])
    .hole(hole_diameter)
)

# Drill a hole through the side face near the right end
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints([( length/2 - end_offset, 0)])
    .hole(hole_diameter)
)