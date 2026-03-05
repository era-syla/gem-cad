import cadquery as cq

# Parametric dimensions for the model
width = 80.0
height = 100.0
thickness = 6.0
wall_thickness = 2.0

# Feature dimensions
chamfer_top_left = 20.0
chamfer_bottom_right = 35.0
fillet_bottom_left = 20.0

# 1. Create base block centered on XY plane
# 2. Apply chamfer to Top-Left corner (Edge at -X, +Y)
# 3. Apply chamfer to Bottom-Right corner (Edge at +X, -Y)
# 4. Apply fillet to Bottom-Left corner (Edge at -X, -Y)
# 5. Shell the object from the top face (>Z) to create the rim and recessed floor

result = (
    cq.Workplane("XY")
    .box(width, height, thickness)
    .edges("|Z and <X and >Y").chamfer(chamfer_top_left)
    .edges("|Z and >X and <Y").chamfer(chamfer_bottom_right)
    .edges("|Z and <X and <Y").fillet(fillet_bottom_left)
    .faces(">Z").shell(-wall_thickness)
)