import cadquery as cq

# Parameters
L_rod = 50.0    # length of single rod
s_rod = 3.0     # cross-section of rod and prongs
s_block = 10.0  # size of central block
L_prong = 40.0  # length of each prong
gap = 2.0       # gap between prongs

# Left single rod (from x = -L_rod to x = 0)
left = (
    cq.Workplane("XY")
    .box(L_rod, s_rod, s_rod, centered=(False, True, True))
    .translate((-L_rod, 0, 0))
)

# Central square block (from x = 0 to x = s_block)
center = (
    cq.Workplane("XY")
    .box(s_block, s_block, s_block, centered=(False, True, True))
)

# Two prongs extending to the right
offset_y = (s_rod + gap) / 2
prong1 = (
    cq.Workplane("XY")
    .box(L_prong, s_rod, s_rod, centered=(False, True, True))
    .translate((s_block, offset_y, 0))
)
prong2 = (
    cq.Workplane("XY")
    .box(L_prong, s_rod, s_rod, centered=(False, True, True))
    .translate((s_block, -offset_y, 0))
)

# Combine all parts into one solid
result = left.union(center).union(prong1).union(prong2)