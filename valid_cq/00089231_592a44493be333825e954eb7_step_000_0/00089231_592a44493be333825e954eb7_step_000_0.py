import cadquery as cq

# Parametric dimensions
height = 100.0         # Total height of the object
outer_diameter = 30.0  # Outer diameter of the cylinder
inner_diameter = 18.0  # Diameter of the center hole
fillet_radius = 4.0    # Radius of the rounded edges

# Generate the CAD model
# 1. Create a base solid cylinder
# 2. Select top and bottom edges and apply a fillet
# 3. Select the top face and cut a through-hole
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(height)
    .edges()
    .fillet(fillet_radius)
    .faces(">Z")
    .hole(inner_diameter)
)