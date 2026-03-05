import cadquery as cq
import math

# Parameters
beam_size = 5.0
length = 200.0
width = 60.0

# Base frame: outer box minus inner cut to form hollow rectangular tube
base = (
    cq.Workplane("XY")
    .box(length, width, beam_size, centered=(True, True, False))
    .faces(">Z")
    .workplane()
    .rect(length - 2 * beam_size, width - 2 * beam_size)
    .cutBlind(beam_size)
)

# Diagonal beams
dx = length - beam_size
dy = width - beam_size
diag_len = math.hypot(dx, dy)
diag_ang = math.degrees(math.atan2(dy, dx))

diag1 = (
    cq.Workplane("XY")
    .box(diag_len, beam_size, beam_size, centered=(True, True, False))
    .rotate((0, 0, 0), (0, 0, 1), diag_ang)
)
diag2 = (
    cq.Workplane("XY")
    .box(diag_len, beam_size, beam_size, centered=(True, True, False))
    .rotate((0, 0, 0), (0, 0, 1), -diag_ang)
)

# Cross beam at mid-length
cross = (
    cq.Workplane("XY")
    .box(beam_size, width - 2 * beam_size, beam_size, centered=(True, True, False))
)

# Back panel (approximate corrugated wall as a thin box)
panel_thickness = 2.0
panel_height = 60.0
panel_y = width / 2 - beam_size / 2 + panel_thickness / 2
panel = (
    cq.Workplane("XY")
    .transformed(offset=(0, panel_y, beam_size))
    .box(length, panel_thickness, panel_height, centered=(True, True, False))
)

# Blocks on the right end: 3 by 2 grid of cubes
block_size = 10.0
blocks_x = 3
blocks_y = 2
total_bx = blocks_x * block_size
total_by = blocks_y * block_size
start_x = length / 2 - beam_size / 2 - total_bx
start_y = width / 2 - beam_size / 2 - total_by

blocks = []
for i in range(blocks_x):
    for j in range(blocks_y):
        cx = start_x + block_size * (i + 0.5)
        cy = start_y + block_size * (j + 0.5)
        blk = (
            cq.Workplane("XY")
            .transformed(offset=(cx, cy, beam_size))
            .box(block_size, block_size, block_size, centered=(True, True, False))
        )
        blocks.append(blk)

# Combine all parts
result = base.union(diag1).union(diag2).union(cross).union(panel)
for b in blocks:
    result = result.union(b)