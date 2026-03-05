import cadquery as cq

# Parameters based on visual estimation of the image
length = 70.0
outer_diameter = 24.0
inner_diameter = 14.0
fillet_radius = 4.0

# Create the model
# Strategy:
# 1. Create a solid cylinder first (this avoids selecting inner edges for the fillet).
# 2. Fillet the outer circular edges.
# 3. Cut the through-hole.
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(length)
    .edges("%CIRCLE")  # Select only circular edges (top and bottom rims)
    .fillet(fillet_radius)
    .faces(">Z")       # Select the top face to start the hole
    .workplane()
    .circle(inner_diameter / 2.0)
    .cutThruAll()      # Cut the hole through the entire length
)