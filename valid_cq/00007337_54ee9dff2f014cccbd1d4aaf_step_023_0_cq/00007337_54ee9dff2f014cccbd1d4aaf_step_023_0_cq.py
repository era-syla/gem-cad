import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0  # Overall outer diameter
height = 20.0          # Height of the ring
thickness = 2.0        # Wall thickness

# Calculate inner radius based on outer diameter and thickness
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - thickness

# Create the cylindrical ring
# Method: Sketch two concentric circles and extrude
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)