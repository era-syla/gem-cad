import cadquery as cq

# Parametric dimensions
total_length = 100
base_height = 15
extrusion_depth = 60

# Profile generation and extrusion
result = (
    cq.Workplane("front")
    .moveTo(0, 0)
    .lineTo(total_length, 0)
    .lineTo(total_length, base_height)
    .lineTo(75, base_height)
    .radiusArc((55, 35), 20)
    .lineTo(35, 35)
    .radiusArc((30, 30), 5)
    .lineTo(30, base_height)
    .lineTo(15, base_height)
    .lineTo(15, 25)
    .lineTo(0, 25)
    .close()
    .extrude(extrusion_depth)
)