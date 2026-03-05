import cadquery as cq

# Main cylindrical body
body_radius = 20
body_length = 35

# Create the main cylinder (axis along X)
result = cq.Workplane("YZ").circle(body_radius).extrude(body_length)

# Add rectangular block on top
block_width = 24
block_height = 12
block_length = 35

top_block = (cq.Workplane("XY")
    .workplane(offset=0)
    .center(body_length/2, 0)
    .rect(body_length, block_width)
    .extrude(block_height)
    .translate((0, 0, body_radius - 2))
)

# Actually build top block differently
top_block = (cq.Workplane("YZ")
    .center(0, body_radius - 2 + block_height/2)
    .rect(block_width, block_height)
    .extrude(body_length)
)

result = result.union(top_block)

# Cut slot down the middle of the top block (groove along X axis)
slot_width = 8
slot_depth = 25

slot_cut = (cq.Workplane("YZ")
    .center(0, body_radius - 2 + block_height/2)
    .rect(slot_width, block_height + 2)
    .extrude(body_length)
)

result = result.cut(slot_cut)

# Cut a through-hole along X axis (bore through cylinder)
bore_radius = 7
result = (result
    .faces(">X")
    .workplane()
    .circle(bore_radius)
    .cutThruAll()
)

# Add counterbore / boss on the front face
boss_outer_radius = 11
boss_inner_radius = bore_radius
boss_depth = 3

boss = (cq.Workplane("YZ")
    .workplane(offset=0)
    .circle(boss_outer_radius)
    .extrude(boss_depth)
)

result = result.union(boss)

# Re-cut the bore through everything
result = (result
    .faces(">X")
    .workplane()
    .circle(bore_radius)
    .cutThruAll()
)

# Cut a rounded slot at the bottom front (the U-shaped cutout visible at bottom right)
u_cut_radius = 6
u_cut = (cq.Workplane("XY")
    .workplane(offset=-(body_radius + 1))
    .center(body_length - 5, 0)
    .circle(u_cut_radius)
    .extrude(body_radius * 2 + 2)
)

result = result.cut(u_cut)

# Cut the vertical slot on the right side going down through the block and into cylinder
side_slot_width = slot_width
side_slot = (cq.Workplane("XZ")
    .workplane(offset=body_length/2)
    .center(0, 0)
    .rect(body_length + 2, body_radius * 2 + block_height)
    .extrude(side_slot_width/2, both=True)
)

# Cut slot from top going down
top_slot = (cq.Workplane("YZ")
    .center(0, 0)
    .rect(slot_width, body_radius * 2 + block_height + 2)
    .extrude(body_length)
)

result = result.cut(top_slot)

# Re-add the bore cut cleanly
result = (result
    .faces(">X")
    .workplane()
    .circle(bore_radius)
    .cutThruAll()
)