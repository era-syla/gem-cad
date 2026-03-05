import cadquery as cq

# Parameters
disc_r = 20
disc_th = 6
block_size = 10
block_len = 15
boss_d = 6
boss_h = 4
shaft_d = 4
shaft_len = 20
pocket_h_y = 12
pocket_d_z = 10
hole_d = 3
hole_r = disc_r - 5

# Main disc, extruded along X, then centered
result = cq.Workplane("YZ").circle(disc_r).extrude(disc_th).translate((-disc_th/2, 0, 0))

# Peripheral holes in the disc
result = result.faces(">X").workplane().pushPoints([
    ( hole_r, 0),
    (-hole_r, 0),
    (0,  hole_r),
    (0, -hole_r),
]).hole(hole_d)

# Top block
block1 = (
    cq.Workplane("XZ")
      .rect(block_size, block_size)
      .extrude(block_len)
      .translate((0, disc_r, 0))
)
result = result.union(block1)

# Bottom block
block2 = (
    cq.Workplane("XZ")
      .rect(block_size, block_size)
      .extrude(-block_len)
      .translate((0, -disc_r, 0))
)
result = result.union(block2)

# Top boss
boss1 = (
    cq.Workplane("XZ", origin=(0, disc_r + block_len, 0))
      .circle(boss_d/2)
      .extrude(boss_h)
)
result = result.union(boss1)

# Bottom boss
boss2 = (
    cq.Workplane("XZ", origin=(0, -disc_r - block_len, 0))
      .circle(boss_d/2)
      .extrude(-boss_h)
)
result = result.union(boss2)

# Shaft protruding from front (positive X)
shaft = (
    cq.Workplane("YZ")
      .circle(shaft_d/2)
      .extrude(shaft_len)
)
result = result.union(shaft)

# Rectangular pocket on one side of the disc
cutter = cq.Workplane("XY").box(disc_th + 2*boss_h, pocket_h_y, pocket_d_z)
cutter = cutter.translate((0, 0, disc_r - pocket_d_z/2))
result = result.cut(cutter)

result