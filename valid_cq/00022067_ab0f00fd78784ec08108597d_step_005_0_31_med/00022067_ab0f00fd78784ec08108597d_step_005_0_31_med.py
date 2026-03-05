import cadquery as cq

# Parametric dimensions
radius = 2.5
length = 100.0

# Create the 3D model (a simple cylindrical rod)
result = (
    cq.Workplane("YZ")
    .circle(radius)
    .extrude(length)
)