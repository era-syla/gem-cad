import cadquery as cq

# Parameters
block_x = 40    # block length along X
block_y = 30    # block width along Y
block_z = 20    # block height along Z
rod_dia = 4     # diameter of guide rods
rod_spacing = 18  # center-to-center spacing of rods in Y
rod_length = 80   # total length of the rods
pocket_z = block_z / 2    # depth of bottom pocket
pocket_w = rod_dia + 2     # width of bottom pocket
chamfer_amt = 4            # chamfer size on front-top edge

# Compute Z offset for the pocket cut
offset_z = -block_z/2 + pocket_z/2

# Build the main block
block = cq.Workplane("XY").box(block_x, block_y, block_z)

# Cut U-shaped pockets for the rods
for y in (rod_spacing/2, -rod_spacing/2):
    pocket = (
        cq.Workplane("XY")
          .transformed(offset=(0, y, offset_z))
          .box(block_x + 2, pocket_w, pocket_z, centered=(True, True, False))
    )
    block = block.cut(pocket)

# Chamfer the front-top edge to create the sloped top face
block = block.edges(">Z and <Y").chamfer(chamfer_amt)

# Create the two guide rods and union them with the block
rods = (
    cq.Workplane("YZ")
      .pushPoints([(0, rod_spacing/2), (0, -rod_spacing/2)])
      .circle(rod_dia/2)
      .extrude(rod_length, both=True)
)

result = block.union(rods)