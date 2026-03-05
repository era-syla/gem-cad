import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0
inner_diameter = 30.0
thickness = 10.0

# Create the ring geometry
# We sketch two concentric circles on the XY plane and extrude them.
# CadQuery automatically detects the region between concentric circles as the face to extrude.
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)