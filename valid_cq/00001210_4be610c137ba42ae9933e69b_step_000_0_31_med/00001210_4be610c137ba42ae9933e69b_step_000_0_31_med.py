import cadquery as cq

# Parametric dimensions
length = 120.0
left_width = 30.0
right_width = 2.0
sag = 15.0
thickness = 20.0

# Create the 3D model
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(0, left_width)
    .lineTo(length, right_width)
    .lineTo(length, 0)
    .threePointArc((length / 2.0, -sag), (0, 0))
    .close()
    .extrude(thickness)
)