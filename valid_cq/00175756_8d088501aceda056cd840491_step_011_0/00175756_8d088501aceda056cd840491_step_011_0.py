import cadquery as cq

# Parametric dimensions for the square post
width = 20.0       # Width of the square cross-section
depth = 20.0       # Depth of the square cross-section
height = 400.0     # Total height/length of the post
fillet_radius = 4.0 # Radius for the rounded corners

# Create the solid geometry
# 1. Start with a 2D rectangle on the XY plane
# 2. Extrude it to create the vertical length
# 3. Select the vertical edges (parallel to Z axis) and apply a fillet
result = (
    cq.Workplane("XY")
    .rect(width, depth)
    .extrude(height)
    .edges("|Z")
    .fillet(fillet_radius)
)