import cadquery as cq

# Parametric dimensions
length = 100.0         # Total length of the tube
outer_diameter = 20.0  # Outer diameter
wall_thickness = 1.0   # Thickness of the tube wall

# Calculate inner radius based on outer diameter and wall thickness
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the tube geometry
# We draw two concentric circles on the XY plane and extrude them.
# CadQuery automatically interprets the space between nested wires as the solid area.
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
)