import cadquery as cq

# Parametric dimensions
diameter = 50.0  # Diameter of the disk
thickness = 5.0  # Thickness of the disk

# Create the cylindrical disk
# 1. Establish a workplane on the XY plane
# 2. Draw a circle with the calculated radius
# 3. Extrude the circle to create a solid cylinder
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(thickness)
)