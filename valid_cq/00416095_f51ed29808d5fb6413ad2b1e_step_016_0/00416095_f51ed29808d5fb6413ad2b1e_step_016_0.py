import cadquery as cq

# Parametric dimensions for the washer
outer_diameter = 30.0  # External diameter of the washer
inner_diameter = 15.0  # Diameter of the central hole
thickness = 3.0        # Thickness of the washer

# Generate the washer geometry
# We create a workplane, draw two concentric circles, and extrude the difference
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)