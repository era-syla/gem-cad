import cadquery as cq

# Parametric dimensions for the washer
outer_diameter = 30.0  # Diameter of the outer edge
inner_diameter = 15.0  # Diameter of the hole
thickness = 3.0        # Thickness of the washer

# Create the washer geometry
# We define a workplane, draw the outer circle, draw the inner circle,
# and extrude. CadQuery automatically subtracts the inner circle from 
# the outer one when extruding concentric profiles.
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)