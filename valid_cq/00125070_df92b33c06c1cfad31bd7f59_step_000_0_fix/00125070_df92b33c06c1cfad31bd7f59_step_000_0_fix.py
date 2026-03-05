import cadquery as cq

# Parameters
H = 20
block_size = 20
wall_thickness = 1.5
rail_thickness = 2
rail_width = 3
outer_x = 80
outer_y = 30
inner_x = outer_x - 2*rail_width
inner_y = outer_y - 2*rail_width
boss_radius = 3
hole_radius = 1

# Vertical offset for rails and bosses so they sit mid-height on the block
z_offset = (H - rail_thickness) / 2

# Central hollow block, hollowed out along the X direction
block = (
    cq.Workplane("XY")
    .box(block_size, block_size, H)
    .faces("|X")
    .shell(-wall_thickness)
)

# Rail outer and inner solids for boolean subtraction
outer_rail = (
    cq.Workplane("XY")
    .workplane(offset=z_offset)
    .rect(outer_x, outer_y)
    .extrude(rail_thickness)
)
inner_rail = (
    cq.Workplane("XY")
    .workplane(offset=z_offset)
    .rect(inner_x, inner_y)
    .extrude(rail_thickness)
)
rails = outer_rail.cut(inner_rail)

# Bosses at the four corners of the outer rail
corner_points = [
    (sx * outer_x / 2, sy * outer_y / 2)
    for sx in (-1, 1)
    for sy in (-1, 1)
]
bosses = (
    cq.Workplane("XY")
    .workplane(offset=z_offset)
    .pushPoints(corner_points)
    .circle(boss_radius)
    .extrude(rail_thickness)
)

# Holes through the bosses
holes = (
    cq.Workplane("XY")
    .workplane(offset=z_offset)
    .pushPoints(corner_points)
    .circle(hole_radius)
    .extrude(rail_thickness)
)

# Combine all parts and subtract holes
result = block.union(rails).union(bosses).cut(holes)