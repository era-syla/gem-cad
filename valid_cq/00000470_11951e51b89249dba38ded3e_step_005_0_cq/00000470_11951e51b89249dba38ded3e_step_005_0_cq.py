import cadquery as cq

# Define parametric dimensions
cylinder_radius = 5.0
cylinder_length = 30.0

# Create the cylinder
# We create a circle on the XY plane and extrude it
result = cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_length)

# Alternatively, using the cylinder primitive directly:
# result = cq.Workplane("XY").cylinder(cylinder_length, cylinder_radius)