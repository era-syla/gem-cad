import cadquery as cq

# Parameters
rod_d = 4
rod_spacing = 20
block_w = rod_spacing + 2*rod_d
block_d = 20
block_h = 6
screw_d = 3
screw_len = 100
slab_thick = 8
hex_nut_w = 8
hex_nut_h = 4

# Positions
bottom_z = block_h/2
top_z = block_h + screw_len + block_h/2
slider_z = (bottom_z + top_z) / 2

# Bottom block
bottom = (
    cq.Workplane("XY")
    .box(block_w, block_d, block_h)
    .translate((0, 0, bottom_z))
    .faces(">Z")
    .workplane()
    .pushPoints([(-rod_spacing/2, 0), (rod_spacing/2, 0)])
    .hole(rod_d)
    .pushPoints([(0, 0)])
    .hole(screw_d)
)

# Top block
top = (
    cq.Workplane("XY")
    .box(block_w, block_d, block_h)
    .translate((0, 0, top_z))
    .faces("<Z")
    .workplane()
    .pushPoints([(-rod_spacing/2, 0), (rod_spacing/2, 0)])
    .hole(rod_d)
    .pushPoints([(0, 0)])
    .hole(screw_d)
)

# Guide rods
rod_length = screw_len + 2*block_h
rod1 = (
    cq.Workplane("XY")
    .circle(rod_d/2)
    .extrude(rod_length)
    .translate(( rod_spacing/2, 0, bottom_z))
)
rod2 = (
    cq.Workplane("XY")
    .circle(rod_d/2)
    .extrude(rod_length)
    .translate((-rod_spacing/2, 0, bottom_z))
)

# Lead screw
screw = (
    cq.Workplane("XY")
    .circle(screw_d/2)
    .extrude(rod_length)
    .translate((0, 0, bottom_z))
)

# Slider block
slider = (
    cq.Workplane("XY")
    .box(block_w, block_d, slab_thick)
    .translate((0, 0, slider_z))
    .faces(">Z")
    .workplane()
    .pushPoints([(-rod_spacing/2, 0), (rod_spacing/2, 0)])
    .hole(rod_d)
    .pushPoints([(0, 0)])
    .hole(screw_d)
)

# Hex nut on screw, captured in slider
nut = (
    cq.Workplane("XY")
    .polygon(6, hex_nut_w)
    .extrude(hex_nut_h)
    .translate((0, 0, slider_z - hex_nut_h/2))
)

# Combine all parts
result = bottom.union(top).union(rod1).union(rod2).union(screw).union(slider).union(nut)