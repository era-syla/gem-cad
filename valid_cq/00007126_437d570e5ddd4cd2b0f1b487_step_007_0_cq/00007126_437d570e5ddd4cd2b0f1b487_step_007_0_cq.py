import cadquery as cq

# Parametric dimensions for the washer
outer_diameter = 20.0  # Outer diameter of the washer
inner_diameter = 10.0  # Inner diameter of the hole
thickness = 2.0        # Thickness of the washer

# Create the washer geometry
# We start with a workplane, draw the outer circle, extrude it, 
# and then cut the inner hole. Alternatively, we can draw two concentric circles 
# and extrude the area between them.

result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)