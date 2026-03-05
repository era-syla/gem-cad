import cadquery as cq

# Define parameters for the disk
diameter = 50.0  # Diameter of the disk
thickness = 5.0  # Thickness of the disk

# Create the disk (cylinder)
# Workplane 'XY' is the standard ground plane.
# circle(radius) draws a circle.
# extrude(distance) pulls that circle into 3D.
result = cq.Workplane("XY").circle(diameter / 2).extrude(thickness)