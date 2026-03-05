import cadquery as cq

# Parametric dimensions based on the visual aspect ratio of the image
width = 50.0       # Dimension along X axis
thickness = 20.0   # Dimension along Y axis
height = 90.0      # Dimension along Z axis
fillet_radius = 2.5 # Radius for the rounded edges

# Generate the 3D model
# 1. Create a box centered on the XY plane
# 2. Select all edges of the box
# 3. Apply a fillet to create rounded corners and edges
result = (
    cq.Workplane("XY")
    .box(width, thickness, height)
    .edges()
    .fillet(fillet_radius)
)