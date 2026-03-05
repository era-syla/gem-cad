import cadquery as cq

# Parametric dimensions
length = 100.0         # Length of the cylinder
outer_diameter = 20.0  # Outer diameter
inner_diameter = 5.0   # Diameter of the central hole

# Create the geometry
# We define a workplane, draw two concentric circles, and extrude them.
# CadQuery automatically interprets the inner circle as a hole when extruding.
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(length)
)