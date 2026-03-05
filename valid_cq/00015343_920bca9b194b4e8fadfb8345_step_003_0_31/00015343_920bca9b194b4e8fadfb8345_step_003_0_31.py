import cadquery as cq

# Dimensions
block_length = 30.0
block_width = 40.0
block_height = 25.0

plate_length = 50.0
plate_thickness = 5.0
plate_radius = 20.0

cutout_x_start = 5.0
cutout_x_end = 25.0
cutout_width = cutout_x_end - cutout_x_start
cutout_bottom_z = 5.0
cutout_vertical_h = 12.0
cutout_arch_z = 22.0

# 1. Base block
block = cq.Workplane("XY").box(
    block_length, 
    block_width, 
    block_height, 
    centered=(False, True, False)
)

# 2. Cutout profile
# Created on XZ plane and extruded through the block's width (Y axis)
cutout = (
    cq.Workplane("XZ")
    .workplane(offset=-block_width/2 - 5)  # Offset slightly outside to ensure a clean cut
    .moveTo(cutout_x_start, cutout_bottom_z)
    .lineTo(cutout_x_end, cutout_bottom_z)
    .lineTo(cutout_x_end, cutout_vertical_h)
    .threePointArc(
        (cutout_x_start + cutout_width/2, cutout_arch_z), 
        (cutout_x_start, cutout_vertical_h)
    )
    .close()
    .extrude(block_width + 10)
)

# Subtract cutout from block
block_with_hole = block.cut(cutout)

# 3. Top plate (straight rectangular section)
plate_straight = (
    cq.Workplane("XY")
    .workplane(offset=block_height)
    .box(
        plate_length, 
        block_width, 
        plate_thickness, 
        centered=(False, True, False)
    )
)

# 4. Top plate (rounded end)
plate_round = (
    cq.Workplane("XY")
    .workplane(offset=block_height)
    .center(plate_length, 0)
    .cylinder(
        plate_thickness, 
        plate_radius, 
        centered=(True, True, False)
    )
)

# Combine all parts into the final solid
result = block_with_hole.union(plate_straight).union(plate_round)