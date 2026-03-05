import cadquery as cq

# Define parametric dimensions
diameter = 100.0  # Diameter of the disk
thickness = 5.0   # Thickness of the disk

# Create the cylindrical disk
# We create a workplane, draw a circle of the specified diameter, and extrude it by the thickness.
result = cq.Workplane("XY").circle(diameter / 2).extrude(thickness)

# Alternatively, a simpler way to create a cylinder directly:
# result = cq.Workplane("XY").cylinder(thickness, diameter / 2)