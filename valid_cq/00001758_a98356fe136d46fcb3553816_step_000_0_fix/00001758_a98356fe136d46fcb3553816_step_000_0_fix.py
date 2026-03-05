import cadquery as cq

# Parameters
length = 80
width = 30
height = 20
channel_width = 10
channel_depth = 15
channel_length = 60
hole_diameter = 8
fillet_radius = 2

result = (
    cq.Workplane("XY")
    .box(width, length, height, centered=(True, True, False))
    .faces(">Z")
    .workplane()
    .transformed(offset=(0, length/2 - channel_length/2))
    .rect(channel_width, channel_length)
    .cutBlind(-channel_depth)
    .faces("<X")
    .workplane()
    .hole(hole_diameter)
    .edges(">Z")
    .fillet(fillet_radius)
)