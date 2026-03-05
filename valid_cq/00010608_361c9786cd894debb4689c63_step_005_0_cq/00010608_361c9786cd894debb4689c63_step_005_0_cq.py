import cadquery as cq

# Parameters
radius = 5.0   # Radius of the cylinder
length = 30.0  # Length of the cylinder

# Create the cylinder
# cq.Workplane("XY") creates a workplane on the XY plane
# .circle(radius) draws a circle with the specified radius
# .extrude(length) extrudes the circle to create the cylinder solid
result = cq.Workplane("XY").circle(radius).extrude(length)

# Alternatively, CadQuery has a built-in primitive for cylinders if a specific orientation isn't needed
# result = cq.Workplane("XY").cylinder(length, radius)