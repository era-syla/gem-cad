import cadquery as cq

# Parametric dimensions
outer_diameter = 20.0
inner_diameter = 10.0
height = 15.0
chamfer_size = 1.0

# Create the basic cylinder
# We start with the outer cylinder and cut the inner hole
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(height)
    .faces(">Z")
    .hole(inner_diameter)
)

# Apply chamfers
# The image shows a clear chamfer on the top outer edge.
# It's common practice for spacers to be symmetric, so applying to bottom as well
# makes sense, though the image only clearly shows the top.
# I will apply it to the top outer edge as distinctly visible.
result = result.edges(">Z and %Circle").chamfer(chamfer_size)

# Optional: If the bottom also looks chamfered (hard to tell for sure but likely), 
# uncomment the following line or combine the selector.
# For this specific image, the top chamfer is the defining feature.
# result = result.edges("<Z and %Circle").chamfer(chamfer_size)