import cadquery as cq

# Parameters
w_bar = 6
t_bar = 3
l_bar = 60
l_small = 10
l_big = 10
plate_th = 2
cyl_r = 3
cyl_l = 15
sep_y = (w_bar + l_big) / 2

# Slender bar
bar = cq.Workplane("XY") \
    .transformed(offset=(l_small + l_bar/2, 0, t_bar/2)) \
    .box(l_bar, w_bar, t_bar)

# Small end block
small_block = cq.Workplane("XY") \
    .transformed(offset=(l_small/2, 0, t_bar + l_small/2)) \
    .box(l_small, l_small, l_small)

# Big blocks
big_block1 = cq.Workplane("XY") \
    .transformed(offset=(l_small + l_bar + l_big/2,  sep_y, t_bar + l_big/2)) \
    .box(l_big, l_big, l_big)
big_block2 = cq.Workplane("XY") \
    .transformed(offset=(l_small + l_bar + l_big/2, -sep_y, t_bar + l_big/2)) \
    .box(l_big, l_big, l_big)

# Plates under big blocks
plate1 = cq.Workplane("XY") \
    .transformed(offset=(l_small + l_bar + l_big/2,  sep_y, t_bar + plate_th/2)) \
    .box(l_big, l_big, plate_th)
plate2 = cq.Workplane("XY") \
    .transformed(offset=(l_small + l_bar + l_big/2, -sep_y, t_bar + plate_th/2)) \
    .box(l_big, l_big, plate_th)

# Cylinders on back of big blocks
cyl1 = cq.Workplane("YZ", origin=(l_small + l_bar + l_big,  sep_y, t_bar + l_big/2)) \
    .circle(cyl_r) \
    .extrude(cyl_l)
cyl2 = cq.Workplane("YZ", origin=(l_small + l_bar + l_big, -sep_y, t_bar + l_big/2)) \
    .circle(cyl_r) \
    .extrude(cyl_l)

# Combine all parts
result = bar.union(small_block) \
            .union(big_block1) \
            .union(big_block2) \
            .union(plate1) \
            .union(plate2) \
            .union(cyl1) \
            .union(cyl2)