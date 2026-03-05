import cadquery as cq

# Parametric dimensions for the cylinder
radius = 10.0   # Radius of the cylinder
height = 50.0   # Height of the cylinder

# Create the cylinder:
# 1. Initialize a Workplane on the XY plane
# 2. Draw a circle with the specified radius
# 3. Extrude the circle by the specified height to create a solid cylinder
result = cq.Workplane("XY").circle(radius).extrude(height)