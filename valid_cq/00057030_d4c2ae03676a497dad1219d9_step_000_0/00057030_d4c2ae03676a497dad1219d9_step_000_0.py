import cadquery as cq

# --- Parametric Dimensions ---
# Base Plate
base_length = 90.0
base_width = 45.0
base_thickness = 5.0

# Vertical Block
block_width = 28.0   # Dimension along Y
block_height = 28.0  # Dimension along Z
block_depth = 20.0   # Dimension along X

# Cylindrical Feature
cyl_diameter = 20.0
cyl_length = 15.0

# Details
hole_diameter = 8.0
slot_width = 2.0

# --- Modeling ---

# 1. Create the Base Plate
# Centered on XY plane for symmetry, thickness centered around Z=0
base = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# Calculate key positions
# Z-height of the top surface of the base
z_top_base = base_thickness / 2.0
# X-position for the center of the block (aligned to one end)
x_block_center = -base_length / 2.0 + block_depth / 2.0
# Z-height of the central axis for the hole and cylinder
z_axis = z_top_base + block_height / 2.0

# 2. Create the Vertical Block
# Positioned on top of the base
block = (
    cq.Workplane("XY")
    .workplane(offset=z_top_base)
    .center(x_block_center, 0)
    .box(block_depth, block_width, block_height, centered=(True, True, False))
)

# 3. Create the Cylindrical Boss
# Extends from the back of the block towards the center of the plate
# Start X is the back face of the block
x_cyl_start = -base_length / 2.0 + block_depth

cylinder = (
    cq.Workplane("YZ")
    .workplane(offset=x_cyl_start)
    .center(0, z_axis)
    .circle(cyl_diameter / 2.0)
    .extrude(cyl_length)
)

# Union the main bodies
result = base.union(block).union(cylinder)

# 4. Cut the Through Hole
# Create a cutter cylinder that goes through the entire length
hole_cutter = (
    cq.Workplane("YZ")
    .workplane(offset=-base_length)
    .center(0, z_axis)
    .circle(hole_diameter / 2.0)
    .extrude(base_length * 2.0)
)
result = result.cut(hole_cutter)

# 5. Cut the Slots (Cross/Collet style) on the Cylinder
# We create two box cutters centered on the cylinder axis
slot_center_x = x_cyl_start + cyl_length / 2.0

# Vertical slot (cuts left/right halves)
slot_v = (
    cq.Workplane("XY")
    .workplane(offset=z_axis)
    .center(slot_center_x, 0)
    .box(cyl_length, slot_width, cyl_diameter * 1.5)
)

# Horizontal slot (cuts top/bottom halves)
slot_h = (
    cq.Workplane("XY")
    .workplane(offset=z_axis)
    .center(slot_center_x, 0)
    .box(cyl_length, cyl_diameter * 1.5, slot_width)
)

result = result.cut(slot_v).cut(slot_h)