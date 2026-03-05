import cadquery as cq

# Define parametric dimensions
length = 50.0  # Length of the cylinder
radius = 5.0   # Radius of the cylinder (diameter = 10.0)

# Create the cylinder
# cq.Workplane("XY") initializes the workplane on the XY plane.
# .circle(radius) creates a 2D circle.
# .extrude(length) extrudes the circle along the Z-axis to create a 3D cylinder.
result = cq.Workplane("XY").circle(radius).extrude(length)