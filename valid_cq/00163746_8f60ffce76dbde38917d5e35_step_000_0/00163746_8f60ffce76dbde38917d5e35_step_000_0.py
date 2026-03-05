import cadquery as cq

# Dimensions
length = 150.0
width = 90.0
thickness = 4.0
notch_width = 8.0
notch_depth = 5.0

# Create the base plate and cut notches
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(0, width / 2), (0, -width / 2)])
    .rect(notch_width, notch_depth * 2)
    .cutThruAll()
)