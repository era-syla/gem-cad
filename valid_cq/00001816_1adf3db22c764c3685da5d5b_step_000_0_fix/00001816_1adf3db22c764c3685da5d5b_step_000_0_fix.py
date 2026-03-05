import cadquery as cq

# Parameters
arm_length = 80
block_length = 30
arm_tip_width = 8
arm_base_width = 12
block_width = 16
thickness = 12
boss_height = 4
boss_length = block_length
boss_width = block_width
ridge_count = 6
ridge_length = 2
ridge_width = boss_width - 4
ridge_height = 2
ridge_spacing = 4

# 2D profile of the lever arm + block
points = [
    (0, -arm_tip_width/2),
    (0,  arm_tip_width/2),
    (arm_length,  arm_base_width/2),
    (arm_length + block_length,  block_width/2),
    (arm_length + block_length, -block_width/2),
    (arm_length, -arm_base_width/2),
    (0, -arm_tip_width/2)
]

# Base extrusion
result = cq.Workplane("XY").polyline(points).close().extrude(thickness)

# Boss on top of block
result = result.faces(">Z").workplane().center(arm_length + boss_length/2, 0).rect(boss_length, boss_width).extrude(boss_height)

# Slot in boss
slot_length = boss_length - 4
slot_width = boss_width - 4
result = result.faces(">Z").workplane().rect(slot_length, slot_width).cutBlind(-boss_height)

# Grip ridges on boss
for i in range(ridge_count):
    x = arm_length + 5 + i * ridge_spacing
    result = result.faces(">Z").workplane().center(x, 0).rect(ridge_length, ridge_width).extrude(ridge_height)

# Circular hole at tip
cyl = cq.Workplane("XY").workplane().center(0, 0).circle(2).extrude(thickness + boss_height + ridge_height + 1)
result = result.cut(cyl)

# Hexagonal hole in side of block
hex_prism = (
    cq.Workplane("XZ")
    .workplane()
    .center(arm_length + block_length/2, thickness/2)
    .polygon(6, 8)
    .extrude(block_width + 2, both=True)
)
result = result.cut(hex_prism)