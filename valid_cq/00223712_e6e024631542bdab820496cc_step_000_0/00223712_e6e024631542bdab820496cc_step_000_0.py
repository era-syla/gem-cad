import cadquery as cq

# --- Parameters ---
# Main plate dimensions
plate_length = 140.0
plate_width = 50.0
plate_thickness = 5.0

# Raised block dimensions
block_length = 35.0
block_width = 38.0
block_height = 10.0  # Height extending above the plate

# Hole dimensions
hole_dia_base = 6.0
hole_dia_block_large = 10.0
hole_dia_block_small = 6.0

# --- Modeling ---

# 1. Create the base plate
# Centered at origin for easier symmetry handling
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Create the raised block
# The block is located at one end (+X) and flush with one side (+Y)
# Calculate center position relative to global origin
block_center_x = (plate_length / 2) - (block_length / 2)
block_center_y = (plate_width / 2) - (block_width / 2)

block = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness / 2)  # Start from top surface of plate
    .moveTo(block_center_x, block_center_y)
    .rect(block_length, block_width)
    .extrude(block_height)
)

# Union the block to the base
result = result.union(block)

# 3. Add holes to the base plate
# Two pairs of holes: one pair near the left end, one pair near the middle
y_margin = 10.0
y_pos = (plate_width / 2) - y_margin

# X positions
x_pos_end = -(plate_length / 2) + 12.0
x_pos_mid = -15.0  # Roughly centered in the exposed flat area

hole_locations = [
    (x_pos_end, y_pos), (x_pos_end, -y_pos),
    (x_pos_mid, y_pos), (x_pos_mid, -y_pos)
]

result = (
    result.faces("<Z").workplane()  # Work from bottom face
    .pushPoints(hole_locations)
    .hole(hole_dia_base)
)

# 4. Add holes to the raised block
# Located on the top face of the block
# The holes are aligned along the block's centerline (Y-axis of block)
# Large hole is inner (left), small hole is outer (right)
hole_spacing = 16.0
x_hole_large = block_center_x - (hole_spacing / 2)
x_hole_small = block_center_x + (hole_spacing / 2)

result = (
    result.faces(">Z").workplane()  # Select the highest face (top of block)
    .moveTo(x_hole_large, block_center_y)
    .hole(hole_dia_block_large)
    .moveTo(x_hole_small, block_center_y)
    .hole(hole_dia_block_small)
)