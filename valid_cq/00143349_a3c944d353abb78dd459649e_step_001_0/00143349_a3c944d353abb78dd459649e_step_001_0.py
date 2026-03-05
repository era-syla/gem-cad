import cadquery as cq

# Parametric dimensions
height = 100.0         # Total height of the cylinder
outer_diameter = 25.0  # External diameter
inner_diameter = 10.0  # Diameter of the central hole

# Create the hollow cylinder geometry
# Method: Sketch two concentric circles on the XY plane and extrude.
# CadQuery interprets the region between the two circles as the solid profile.
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(height)
)