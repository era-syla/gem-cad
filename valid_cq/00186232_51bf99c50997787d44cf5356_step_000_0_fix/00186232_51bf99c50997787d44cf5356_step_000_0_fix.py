import cadquery as cq

# Parameters
plate_x, plate_y, plate_thk = 120, 60, 4
tube_r = 3
block_x, block_y, block_z = 20, 40, 15
sup_base, sup_h, sup_w = 10, 15, 15

# Top plate
plate = cq.Workplane("XY") \
    .box(plate_x, plate_y, plate_thk, centered=(True, True, False)) \
    .translate((0, 0, block_z))

# Bumper around plate
bumper = cq.Workplane("XY") \
    .box(plate_x + 2 * tube_r, plate_y + 2 * tube_r, 2 * tube_r, centered=(True, True, False)) \
    .edges("|Z").fillet(tube_r) \
    .translate((0, 0, block_z + plate_thk))

# Central mounting block underneath
block = cq.Workplane("XY") \
    .box(block_x, block_y, block_z, centered=(True, True, False))

# Triangular support 1 on +Y side
sup1 = cq.Workplane("XZ") \
    .transformed(offset=(block_x/2, block_y/4 - sup_w/2, 0)) \
    .polyline([(0, 0), (sup_base, 0), (sup_base, sup_h)]) \
    .close() \
    .extrude(sup_w)

# Triangular support 2 on -Y side
sup2 = cq.Workplane("XZ") \
    .transformed(offset=(block_x/2, -block_y/4 - sup_w/2, 0)) \
    .polyline([(0, 0), (sup_base, 0), (sup_base, sup_h)]) \
    .close() \
    .extrude(sup_w)

# Combine all parts
result = plate.union(bumper).union(block).union(sup1).union(sup2)