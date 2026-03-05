import cadquery as cq

# Main lever/latch component
# The part has a curved arm on the left tapering to a point,
# and a rectangular block on the right with serrations on top

# Overall dimensions estimate:
# Total length ~120mm, height ~20mm, width ~15mm

# Build the main body profile as a 2D shape, then extrude

# Create the main flat body - a swept/tapered arm shape
# The arm tapers from the block end to a rounded tip

import cadquery as cq
from cadquery import Edge, Wire, Face, Solid

# Main rectangular block portion (right side)
block_length = 40
block_height = 18
block_width = 15
block_x_start = 0

# Arm portion (left side) - tapers to a point
arm_length = 80
arm_height_at_block = 12
arm_height_at_tip = 8

# Create the profile in XY plane, then extrude in Z

# Profile points for the side view (XY plane)
# Right side is the block, left side tapers
profile_pts = [
    (0, 0),           # bottom right of block
    (block_length, 0),  # bottom right end of block  
    (block_length, block_height),  # top right end
    (0, block_height),  # top left of block
    (0, arm_height_at_block),  # transition to arm top
    (-arm_length, arm_height_at_tip/2 + 1),  # arm top left near tip
    (-arm_length - 5, arm_height_at_tip/2),  # tip top
    (-arm_length - 8, 0),  # tip point (rounded later)
    (-arm_length - 5, -arm_height_at_tip/2),  # tip bottom
    (-arm_length, -arm_height_at_tip/2 - 1),  # arm bottom left near tip
    (0, -2),          # arm bottom right
    (0, 0),           # close
]

# Build using polyline with arcs for the tip
result = (
    cq.Workplane("XY")
    .moveTo(profile_pts[0][0], profile_pts[0][1])
    .polyline(profile_pts[1:])
    .close()
    .extrude(block_width)
)

# Add the rectangular block - make it slightly wider/taller on right side
block = (
    cq.Workplane("XY")
    .rect(block_length, block_height + 4)
    .extrude(block_width)
    .translate((block_length/2, (block_height + 4)/2 - 2, 0))
)

# Union block with result
result = result.union(block)

# Add serrations on top of block
serration_count = 5
serration_width = 2
serration_height = 2
serration_depth = block_width * 0.8

for i in range(serration_count):
    x_pos = block_length - 5 - i * (serration_width * 1.5)
    serration = (
        cq.Workplane("XY")
        .box(serration_width, serration_height, serration_depth)
        .translate((x_pos, block_height + 2 + serration_height/2, block_width/2))
    )
    result = result.union(serration)

# Add pivot hole at the tip of the arm
pivot_x = -arm_length - 3
pivot_y = 0
pivot_r = 3

result = (
    result
    .cut(
        cq.Workplane("XY")
        .circle(pivot_r)
        .extrude(block_width)
        .translate((pivot_x, pivot_y, 0))
    )
)

# Add a screw hole in the block
screw_hole = (
    cq.Workplane("XY")
    .circle(3)
    .extrude(block_width)
    .translate((block_length * 0.6, block_height/2, 0))
)
result = result.cut(screw_hole)

# Add channel/slot on top of arm near block
channel = (
    cq.Workplane("XY")
    .box(15, 4, block_width * 0.6)
    .translate((-5, arm_height_at_block - 2, block_width/2))
)
result = result.cut(channel)

# Fillet some edges to smooth the model
try:
    result = result.edges("|Z").fillet(1.5)
except:
    pass