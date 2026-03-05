import cadquery as cq

# Parametric dimensions
height = 20.0  # Height of the cylinder
radius = 5.0   # Radius of the cylinder

# Create the cylinder
# We create a workplane, sketch a circle, and extrude it
result = cq.Workplane("XY").circle(radius).extrude(height)

# Alternative method (direct solid creation):
# result = cq.Solid.makeCylinder(radius, height)