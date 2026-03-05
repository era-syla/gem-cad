import cadquery as cq

# Parametric dimensions
radius = 20.0
height = 40.0

# Create the cylinder
# cq.Workplane("XY") sets the drawing plane
# .circle(radius) draws a 2D circle
# .extrude(height) creates the solid cylinder
result = cq.Workplane("XY").circle(radius).extrude(height)