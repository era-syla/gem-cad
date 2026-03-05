import cadquery as cq

# --- Parametric Dimensions ---
# Main plate dimensions
length = 400.0
width = 100.0
thickness = 8.0
corner_fillet = 5.0

# Large hole dimensions (the two main cutouts)
large_hole_diameter = 45.0
large_hole_separation = 280.0  # Distance between centers

# Corner mounting holes dimensions
mounting_hole_diameter = 6.0
mounting_dx = 370.0  # Distance between centers in X
mounting_dy = 80.0   # Distance between centers in Y

# Center grid pattern dimensions
center_hole_diameter = 5.0
grid_cols = 3
grid_rows = 2
grid_spacing_x = 20.0
grid_spacing_y = 20.0

# --- Geometry Generation ---

# 1. Create base plate with rounded corners
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(corner_fillet)
)

# 2. Cut the two large holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-large_hole_separation / 2, 0), (large_hole_separation / 2, 0)])
    .hole(large_hole_diameter)
)

# 3. Cut the 4 corner mounting holes
result = (
    result.faces(">Z")
    .workplane()
    .rect(mounting_dx, mounting_dy, forConstruction=True)
    .vertices()
    .hole(mounting_hole_diameter)
)

# 4. Cut the center grid of holes
result = (
    result.faces(">Z")
    .workplane()
    .rarray(grid_spacing_x, grid_spacing_y, grid_cols, grid_rows)
    .hole(center_hole_diameter)
)