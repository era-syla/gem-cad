import cadquery as cq

# Define parametric dimensions
cylinder_radius = 10.0
cylinder_height = 40.0

# Create the cylinder
# We start on the XY plane, draw a circle, and extrude it vertically
result = (
    cq.Workplane("XY")
    .circle(cylinder_radius)
    .extrude(cylinder_height)
)