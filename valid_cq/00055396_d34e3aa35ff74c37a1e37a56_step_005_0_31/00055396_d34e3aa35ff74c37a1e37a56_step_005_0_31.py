import cadquery as cq

# Parametric dimensions
length = 100.0
height = 50.0
width = 25.0
thickness = 2.0

# Create the L-bracket profile and extrude
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),
        (-width, 0),
        (-width, thickness),
        (-thickness, thickness),
        (-thickness, height),
        (0, height)
    ])
    .close()
    .extrude(length)
)