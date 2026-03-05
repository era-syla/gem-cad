import cadquery as cq

outer_x = 120
outer_y = 60
thickness = 5
border = 5
pocket_depth = 2

pad_big_w = 15
pad_big_h = 8
pad_small_w = 8
pad_small_h = 4

vert_spacing = 20
horiz_spacing = 10
cols_small = 6

# Create base plate
result = cq.Workplane("XY").box(outer_x, outer_y, thickness)

# Pocket on top face
result = result.faces(">Z").workplane().rect(outer_x - 2*border, outer_y - 2*border).cutBlind(-pocket_depth)

# Z coordinate of pocket floor
z0 = thickness - pocket_depth

# Positions for pads
y_top = vert_spacing/2
y_bottom = -vert_spacing/2
x_big = -outer_x/2 + border + pad_big_w/2
x_small0 = -outer_x/2 + border + pad_small_w/2
x_start_small = -outer_x/2 + border + pad_big_w + horiz_spacing + pad_small_w/2

# Big pad (top-left)
pad = cq.Workplane("XY", origin=(0,0,z0)).center(x_big, y_top).rect(pad_big_w, pad_big_h).extrude(pocket_depth)
result = result.union(pad)

# Small pad under big (bottom-left)
pad = cq.Workplane("XY", origin=(0,0,z0)).center(x_small0, y_bottom).rect(pad_small_w, pad_small_h).extrude(pocket_depth)
result = result.union(pad)

# Remaining small pads in two rows
for i in range(cols_small):
    x = x_start_small + i*(pad_small_w + horiz_spacing)
    for y in (y_top, y_bottom):
        pad = cq.Workplane("XY", origin=(0,0,z0)).center(x, y).rect(pad_small_w, pad_small_h).extrude(pocket_depth)
        result = result.union(pad)