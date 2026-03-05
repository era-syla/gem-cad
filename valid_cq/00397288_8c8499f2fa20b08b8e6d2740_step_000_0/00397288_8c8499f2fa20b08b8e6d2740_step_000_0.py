import cadquery as cq

# Define dimensions
length = 80.0
width = 40.0
thickness = 3.0
corner_radius = 4.0
edge_fillet = 1.0

# Create the model
# 1. Generate the base rectangular plate
# 2. Apply fillets to the vertical corners
# 3. Apply fillets to the top and bottom edges
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")  # Select vertical edges
    .fillet(corner_radius)
    .edges("#Z")  # Select edges perpendicular to Z (top and bottom perimeters)
    .fillet(edge_fillet)
)