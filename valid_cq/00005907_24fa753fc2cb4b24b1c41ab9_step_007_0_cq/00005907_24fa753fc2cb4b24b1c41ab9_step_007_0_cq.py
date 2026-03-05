import cadquery as cq

# Define parametric dimensions
radius = 10.0  # Radius of the cylinder
height = 3.0   # Height/thickness of the cylinder

# Create the cylinder
# Workplane("XY") starts on the standard XY plane
# circle(radius) draws a circle profile
# extrude(height) extrudes the profile to create a solid cylinder
result = cq.Workplane("XY").circle(radius).extrude(height)