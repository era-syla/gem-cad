import cadquery as cq

# Basic dimensions
thickness = 10
hole_diameter = 5

# Create main V shape
v_shape = (
    cq.Workplane("XY")
    .lineTo(20, 0)
    .lineTo(30, 30)
    .lineTo(0, 30)
    .close()
    .extrude(thickness)
)

# Locate holes
holes = (
    v_shape.faces(">Z")
    .workplane()
    .pushPoints([(10, 5), (22, 25), (5, 25)])
    .hole(hole_diameter)
)

result = holes

