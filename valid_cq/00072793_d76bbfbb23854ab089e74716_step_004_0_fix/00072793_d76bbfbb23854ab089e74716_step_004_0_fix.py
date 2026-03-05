import cadquery as cq

# Parameters
L = 100
W = 60
base_th = 3
wall_h = 15
wall_th = base_th
tab_h = 10
tab_x = 20

# Base plate
base = cq.Workplane("XY").box(L, W, base_th, centered=(True, True, False))

# End walls
wall1 = cq.Workplane("XY").box(L, wall_th, wall_h, centered=(True, True, False)) \
    .translate((0,  W/2 - wall_th/2, base_th))
wall2 = cq.Workplane("XY").box(L, wall_th, wall_h, centered=(True, True, False)) \
    .translate((0, -W/2 + wall_th/2, base_th))

# Downward tab at front center
tab = cq.Workplane("XY").box(tab_x, wall_th, tab_h, centered=(True, True, False)) \
    .translate((0, -W/2 + wall_th/2, -tab_h))

# Combine all parts
result = base.union(wall1).union(wall2).union(tab)