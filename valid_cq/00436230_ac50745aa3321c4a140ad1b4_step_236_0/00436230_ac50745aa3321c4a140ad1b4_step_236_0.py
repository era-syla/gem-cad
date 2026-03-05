import cadquery as cq

# Parametric dimensions
diameter = 100.0  # Diameter of the circular disk
thickness = 2.0   # Thickness of the disk

# Create the solid geometry
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(thickness)
)