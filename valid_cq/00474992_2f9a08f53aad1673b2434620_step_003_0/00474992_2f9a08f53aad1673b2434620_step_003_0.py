import cadquery as cq

# Parametric dimensions
length = 100.0
width = 40.0
thickness = 10.0
fillet_radius = 4.0

# Create the model: A rectangular bar with filleted top edges
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|X and >Z")  # Select edges parallel to X-axis located at the top (max Z)
    .fillet(fillet_radius)
)