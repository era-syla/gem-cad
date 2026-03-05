import cadquery as cq

# Parametric dimensions for the hollow cylinder
height = 100.0         # Height of the tube
outer_diameter = 30.0  # External diameter
wall_thickness = 2.0   # Wall thickness

# derived calculations
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the model
# 1. Start on XY plane
# 2. Draw outer circle
# 3. Draw inner circle (CadQuery interprets nested closed wires as holes during extrusion)
# 4. Extrude to create the solid tube
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)