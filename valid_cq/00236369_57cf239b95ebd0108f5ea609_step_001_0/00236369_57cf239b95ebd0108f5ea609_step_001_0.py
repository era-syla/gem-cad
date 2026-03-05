import cadquery as cq

# Parametric dimensions based on visual estimation
length = 400.0
width = 30.0
thickness = 5.0
hole_diameter = 6.0
hole_margin = 15.0  # Distance from the end edge to the center of the hole

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-(length / 2 - hole_margin), 0),
        ((length / 2 - hole_margin), 0)
    ])
    .hole(hole_diameter)
)