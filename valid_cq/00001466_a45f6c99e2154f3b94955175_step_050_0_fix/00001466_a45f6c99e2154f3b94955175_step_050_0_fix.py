import cadquery as cq

# Parameters
block_x = 25
block_y = 15
block_z = 15

foot_w = 4
foot_d = 6
foot_h = 4

hole_d = 6
hole_depth = block_y + 2

n_fins = 12
fin_thick = 1.2
fin_gap = 1.0
outer_r = 10
inner_r = 3

disc1_r = 11
disc1_h = 2
disc2_r = 8
disc2_h = 3
disc3_r = 12
disc3_h = 2

# Build base block with side hole and feet
result = (
    cq.Workplane("XY")
    .box(block_x, block_y, block_z)
    .faces(">Y").workplane()
    .hole(hole_d, hole_depth)
    .faces("<Z").workplane()
    .pushPoints([
        (-(block_x/2 - foot_w/2), (block_y/2 - foot_d/2)),
        ( (block_x/2 - foot_w/2), (block_y/2 - foot_d/2))
    ])
    .rect(foot_w, foot_d)
    .extrude(-foot_h)
)

# Build fin stack
block_top = block_z/2
for i in range(n_fins):
    z = block_top + i * (fin_thick + fin_gap)
    ring = (
        cq.Workplane("XY")
        .workplane(offset=z)
        .circle(outer_r)
        .circle(inner_r)
        .extrude(fin_thick)
    )
    result = result.union(ring)

# Build stepped top discs
z1 = block_top + n_fins * (fin_thick + fin_gap)
disc1 = (
    cq.Workplane("XY")
    .workplane(offset=z1)
    .circle(disc1_r)
    .circle(inner_r)
    .extrude(disc1_h)
)
result = result.union(disc1)

z2 = z1 + disc1_h
disc2 = (
    cq.Workplane("XY")
    .workplane(offset=z2)
    .circle(disc2_r)
    .circle(inner_r)
    .extrude(disc2_h)
)
result = result.union(disc2)

z3 = z2 + disc2_h
disc3 = (
    cq.Workplane("XY")
    .workplane(offset=z3)
    .circle(disc3_r)
    .circle(inner_r)
    .extrude(disc3_h)
)
result = result.union(disc3)