import cadquery as cq

# Parametric dimensions
diameter = 100.0  # Diameter of the disk
thickness = 10.0  # Thickness of the disk

# Create the cylindrical disk
# 1. Select the XY workplane
# 2. Draw a circle with the specified radius
# 3. Extrude it to create the solid thickness
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(thickness)
)