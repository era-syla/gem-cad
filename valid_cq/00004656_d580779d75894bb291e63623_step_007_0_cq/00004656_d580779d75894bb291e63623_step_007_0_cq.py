import cadquery as cq

# Define parameters for the cylinder
length = 50.0   # Length of the cylinder
diameter = 25.0 # Diameter of the cylinder
radius = diameter / 2.0

# Create the cylinder
# Workplane 'XY' creates a plane on the XY axes.
# .circle(radius) draws a circle on that plane.
# .extrude(length) extrudes the circle along the normal (Z-axis) to create a cylinder.
result = cq.Workplane("XY").circle(radius).extrude(length)

# Alternatively, CadQuery has a built-in solid creation method for simple primitives like cylinders
# result = cq.Workplane("XY").cylinder(height=length, radius=radius)