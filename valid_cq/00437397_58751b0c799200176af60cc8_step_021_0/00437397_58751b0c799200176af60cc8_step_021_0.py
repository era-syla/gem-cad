import cadquery as cq

# Parametric dimensions
outer_diameter = 30.0
inner_diameter = 12.0
thickness = 3.0

# Create the washer
# We draw two concentric circles on the XY plane and extrude them.
# CadQuery automatically interprets the area between concentric circles as the solid profile.
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)