import cadquery as cq

# -- Parameters --
plate_size = 100.0      # Width and length of the square plate
plate_thickness = 10.0  # Thickness of the plate
groove_width = 8.0      # Width of the grid cuts
groove_depth = 3.0      # Depth of the cuts / thickness of the floating grid

# -- Calculations --
# We assume a 3x3 grid pattern with equal sized square tiles
# Total width = 3 * tile_width + 2 * groove_width
tile_width = (plate_size - 2 * groove_width) / 3.0

# Calculate the offset from the center to the groove center lines
# The middle tile is centered at 0, with width 'tile_width'.
# The groove center is at (tile_width/2) + (groove_width/2)
offset_dist = (tile_width + groove_width) / 2.0
offsets = [-offset_dist, offset_dist]

# -- Part 1: Bottom-Left Grooved Plate --

# 1. Create Base Plate
# Centered at the origin
base = cq.Workplane("XY").box(plate_size, plate_size, plate_thickness)

# 2. Create Cutter Geometry
# The cutter needs to be slightly longer than the plate to ensure clean through-cuts on the edges
cut_len = plate_size + 10.0

# Define bars along X (spaced in Y)
cut_x = (
    cq.Workplane("XY")
    .pushPoints([(0, y) for y in offsets])
    .box(cut_len, groove_width, groove_depth)
)

# Define bars along Y (spaced in X)
cut_y = (
    cq.Workplane("XY")
    .pushPoints([(x, 0) for x in offsets])
    .box(groove_width, cut_len, groove_depth)
)

# Combine into a single cutter object
cutter = cut_x.union(cut_y)

# 3. Apply Cut
# The plate is centered at Z=0, so its top face is at Z = plate_thickness/2.
# We want the groove to start at the top face and go down by 'groove_depth'.
# The cutter box is centered vertically, so we position its center at:
# Z = (Top Face) - (Half Groove Depth)
cutter_z = (plate_thickness / 2.0) - (groove_depth / 2.0)
cutter_positioned = cutter.translate((0, 0, cutter_z))

plate = base.cut(cutter_positioned)

# -- Part 2: Top-Right Grid Object --

# Create the grid geometry matching the plate size (exact length, not oversized)
grid_x = (
    cq.Workplane("XY")
    .pushPoints([(0, y) for y in offsets])
    .box(plate_size, groove_width, groove_depth)
)

grid_y = (
    cq.Workplane("XY")
    .pushPoints([(x, 0) for x in offsets])
    .box(groove_width, plate_size, groove_depth)
)

grid_object = grid_x.union(grid_y)

# Position the grid relative to the plate to match the image
# Floating to the right and back
grid_scene_pos = grid_object.translate((plate_size * 1.5, plate_size * 0.8, plate_size * 0.5))

# -- Final Result --
# Combine both objects into the final assembly
result = plate.union(grid_scene_pos)