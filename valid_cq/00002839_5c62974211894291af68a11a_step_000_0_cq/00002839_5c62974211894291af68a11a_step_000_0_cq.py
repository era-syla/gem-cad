import cadquery as cq

# Parameters for the gauge block set
# Based on visual estimation of relative sizes
block_width = 10.0
block_height = 10.0
block_length = 30.0
gap_size = 5.0
num_blocks = 9

# Parameters for the drill/gauge plate
plate_size = 40.0
plate_thickness = 10.0
plate_offset = 10.0  # Distance from the last block

# Gauge block set (the linear array of rectangular blocks)
# We create a series of blocks spaced apart
blocks = cq.Workplane("XY")

for i in range(num_blocks):
    # Calculate the center position for each block
    # We place them along the X-axis
    x_pos = i * (block_width + gap_size)
    
    # Create a single block at the calculated position
    current_block = (
        cq.Workplane("XY")
        .center(x_pos, 0)
        .box(block_width, block_length, block_height)
    )
    
    if i == 0:
        blocks = current_block
    else:
        blocks = blocks.union(current_block)

# Drill/Hole Gauge Plate (the square block with holes)
# Position it to the right of the blocks
plate_center_x = (num_blocks * (block_width + gap_size)) + (plate_size / 2.0) - gap_size + plate_offset
plate_center_y = 0

plate_solid = (
    cq.Workplane("XY")
    .center(plate_center_x, plate_center_y)
    .box(plate_size, plate_size, plate_thickness)
)

# Adding holes to the plate
# The holes appear to be of varying sizes, arranged somewhat spirally or by size
# Let's approximate the hole pattern seen in the image (largest to smallest)
# Coordinates are relative to the plate center

holes = [
    # (x_rel, y_rel, diameter)
    (-8, 8, 12),    # Top Left (Largest)
    (8, 8, 10),     # Top Right
    (-10, -5, 8),   # Mid Left
    (0, 0, 7),      # Center
    (12, -2, 6),    # Mid Right
    (-6, -14, 5),   # Bottom Left
    (4, -12, 4),    # Bottom Mid
    (10, -14, 3),   # Bottom Right small
    (8, -8, 2),     # Tiny one
]

plate_with_holes = plate_solid
for hx, hy, dia in holes:
    # Use cutBlind to ensure it goes through, but just cutThruAll is safer given the context
    plate_with_holes = (
        plate_with_holes.faces(">Z")
        .workplane()
        .center(hx, hy)
        .hole(dia)
    )

# Combine both main parts into the final result
result = blocks.union(plate_with_holes)