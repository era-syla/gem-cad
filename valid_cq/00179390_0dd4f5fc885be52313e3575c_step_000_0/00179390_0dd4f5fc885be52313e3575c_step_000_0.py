import cadquery as cq

# --- Parameters ---

# Rear Plate Dimensions
plate_width = 85.0
plate_height = 50.0
plate_thickness = 2.0
plate_fillet_radius = 6.0

# Front Block Dimensions
block_width = 65.0
block_height = 40.0
block_thickness = 8.0

# Grid Pattern Dimensions
grid_cols = 7
grid_rows = 4
grid_pitch_x = 6.5  # Spacing between columns
grid_pitch_y = 6.5  # Spacing between rows
grid_hole_dia = 2.8

# Mounting Hole Dimensions
mount_hole_dia = 3.2
mount_cb_dia = 5.5   # Counterbore diameter
mount_cb_depth = 2.5 # Counterbore depth
# Offsets from center for mounting holes
mount_offset_x = 27.0
mount_offset_y = 15.0

# --- Modeling ---

# 1. Create the base rear plate
# Centered on the XY plane
base = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .edges("|Z")
    .fillet(plate_fillet_radius)
)

# 2. Add the front rectangular block
# Extrude from the front face of the base plate
block = (
    base.faces(">Z")
    .workplane()
    .rect(block_width, block_height)
    .extrude(block_thickness)
)

# 3. Cut the grid of holes
# rarray creates a centered rectangular array of points
block_with_grid = (
    block.faces(">Z")
    .workplane()
    .rarray(grid_pitch_x, grid_pitch_y, grid_cols, grid_rows)
    .hole(grid_hole_dia)
)

# 4. Cut the mounting holes
# Located at Top-Left and Bottom-Right corners of the block face
# Coordinates are relative to the center of the workplane
mount_points = [
    (-mount_offset_x, mount_offset_y),  # Top-Left
    (mount_offset_x, -mount_offset_y)   # Bottom-Right
]

result = (
    block_with_grid.faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .cboreHole(mount_hole_dia, mount_cb_dia, mount_cb_depth)
)