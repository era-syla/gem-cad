import cadquery as cq

# -- Parametric Dimensions --
length = 50.0       # Length of the cylinder
outer_diameter = 40.0 # Outer diameter
wall_thickness = 5.0  # Thickness of the tube wall

# Calculated inner diameter
inner_diameter = outer_diameter - (2 * wall_thickness)

# -- Modeling --
# Create the main cylinder
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(length)
)
