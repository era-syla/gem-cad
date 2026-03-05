import cadquery as cq

# --- Parameters ---

# Base Plate Dimensions
plate_length = 120.0
plate_width = 60.0
plate_thickness = 2.0

# Large Block (Bottom Left)
block1_w = 24.0
block1_d = 20.0
block1_h = 4.0
block1_center = (-35, -10)

# Medium Block (Top Left)
block2_w = 14.0
block2_d = 10.0
block2_h = 3.0
block2_center = (-35, 15)

# Small Square 1 (Top Middle)
block3_size = 10.0
block3_h = 3.0
block3_center = (-5, 18)

# Small Square 2 (Right Middle)
block4_size = 10.0
block4_h = 3.0
block4_center = (12, 12)

# Octagon (Center)
oct_diameter = 6.0
oct_height = 2.0
oct_center = (2, 0)

# Angled Block (Right Side)
block5_w = 18.0
block5_d = 28.0
block5_h = 4.0
block5_center = (40, -5)
block5_angle = -35.0  # Degrees rotation

# --- Modeling ---

# 1. Create Base Plate
# Centered at origin, Z range [-thickness/2, thickness/2]
base = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Calculate Z-level for components to sit on top of the plate
top_z = plate_thickness / 2.0

# 2. Create Large Block
b1 = (
    cq.Workplane("XY")
    .box(block1_w, block1_d, block1_h)
    .translate((block1_center[0], block1_center[1], top_z + block1_h / 2.0))
)

# 3. Create Medium Block
b2 = (
    cq.Workplane("XY")
    .box(block2_w, block2_d, block2_h)
    .translate((block2_center[0], block2_center[1], top_z + block2_h / 2.0))
)

# 4. Create Small Square 1
b3 = (
    cq.Workplane("XY")
    .box(block3_size, block3_size, block3_h)
    .translate((block3_center[0], block3_center[1], top_z + block3_h / 2.0))
)

# 5. Create Small Square 2
b4 = (
    cq.Workplane("XY")
    .box(block4_size, block4_size, block4_h)
    .translate((block4_center[0], block4_center[1], top_z + block4_h / 2.0))
)

# 6. Create Central Octagon
# Using polygon and extrude. We start the workplane on top of the base.
octagon = (
    cq.Workplane("XY")
    .workplane(offset=top_z)
    .center(oct_center[0], oct_center[1])
    .polygon(8, oct_diameter)
    .extrude(oct_height)
)

# 7. Create Angled Block
# Create at origin to rotate around center, then translate to position
b5 = (
    cq.Workplane("XY")
    .box(block5_w, block5_d, block5_h)
    .rotate((0, 0, 1), (0, 0, 0), block5_angle)
    .translate((block5_center[0], block5_center[1], top_z + block5_h / 2.0))
)

# --- Combine into Final Result ---
result = (
    base
    .union(b1)
    .union(b2)
    .union(b3)
    .union(b4)
    .union(octagon)
    .union(b5)
)