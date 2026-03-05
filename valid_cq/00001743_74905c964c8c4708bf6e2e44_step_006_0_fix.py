import cadquery as cq

# Main rectangular block/connector at the right end
block_width = 8
block_height = 12
block_depth = 6

# Thin rod extending to the left
rod_diameter = 2
rod_length = 80

# Transition/taper piece connecting rod to block
taper_length = 10

# Build the block
block = (
    cq.Workplane("XY")
    .box(block_depth, block_width, block_height)
)

# Build the rod - extending from the left face of the block
rod = (
    cq.Workplane("YZ")
    .center(0, 0)
    .workplane(offset=-(block_depth/2 + rod_length))
    .circle(rod_diameter / 2)
    .extrude(rod_length)
)

# Build a taper/transition from rod to block
# The taper connects the rod end to the block face
taper = (
    cq.Workplane("XY")
    .center(-(block_depth/2 + taper_length/2), 0)
    .box(taper_length, rod_diameter * 2, rod_diameter * 2)
)

# Alternative approach: build everything from scratch cleanly
# Block at origin
result_block = cq.Workplane("XY").box(block_depth, block_width, block_height)

# Rod along X axis, extending to the negative X direction
result_rod = (
    cq.Workplane("YZ")
    .circle(rod_diameter / 2)
    .extrude(rod_length)
    .translate((-block_depth/2 - rod_length, 0, 0))
)

# Small transition box
result_taper = (
    cq.Workplane("XY")
    .box(taper_length, rod_diameter * 1.5, rod_diameter * 1.5)
    .translate((-(block_depth/2 + taper_length/2), 0, 0))
)

# Combine all parts
result = (
    result_block
    .union(result_rod)
    .union(result_taper)
)