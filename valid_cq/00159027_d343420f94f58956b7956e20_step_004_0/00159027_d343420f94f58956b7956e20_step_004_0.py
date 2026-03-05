import cadquery as cq

# Parametric dimensions
cylinder_radius = 5.0
cylinder_height = 80.0

# Create the 3D model
# Start with the XY plane, draw the circular profile, and extrude to height
result = (
    cq.Workplane("XY")
    .circle(cylinder_radius)
    .extrude(cylinder_height)
)