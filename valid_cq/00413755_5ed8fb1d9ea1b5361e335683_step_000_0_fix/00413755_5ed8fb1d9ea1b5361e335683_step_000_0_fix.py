import cadquery as cq

# Base dimensions
length = 150.0
width = 70.0
height = 10.0
corner_radius = 5.0
thickness = 2.0
cutout_radius = 7.0
cutout_position = 130.0

# Create the base
result = (
    cq.Workplane("XY")
    .box(length, width, height, centered=(True, True, False))
    .edges("|Z").fillet(corner_radius)
    .faces(">Z").shell(-thickness)
    .faces(">Z").workplane()
    .center(length / 2 - cutout_position, 0)
    .circle(cutout_radius)
    .cutThruAll()
)