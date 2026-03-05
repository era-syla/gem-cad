import cadquery as cq

# Parametric dimensions
outer_diameter = 20.0  # Diameter of the main cylinder
inner_diameter = 8.0   # Diameter of the through-hole
height = 30.0          # Total height of the spacer
chamfer_size = 0.5     # Size of the chamfer on the hole edges

# Create the main cylinder
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(height)
)

# Cut the through-hole
result = (
    result.faces(">Z")
    .workplane()
    .hole(inner_diameter)
)

# Apply chamfer to the top and bottom edges of the hole
# Selecting edges that belong to the inner cylinder face
result = result.edges(cq.selectors.RadiusNthSelector(0)).chamfer(chamfer_size)