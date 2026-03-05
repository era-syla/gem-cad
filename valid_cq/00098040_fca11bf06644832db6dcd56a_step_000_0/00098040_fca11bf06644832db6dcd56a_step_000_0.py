import cadquery as cq

# Parametric dimensions
diameter = 100.0  # Diameter of the disk
thickness = 5.0   # Thickness of the disk

# Create the disk geometry
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(thickness)
)