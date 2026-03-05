import cadquery as cq

# Parameters
center_dist = 60
bar_width = 8
thickness = 4
boss_r = 6
pocket_r = 3
pocket_depth = 2

# Rectangular bar
bar = cq.Workplane("XY").rect(center_dist, bar_width).extrude(thickness)

# End bosses
boss = cq.Workplane("XY").circle(boss_r).extrude(thickness)
boss1 = boss.translate((center_dist/2, 0, 0))
boss2 = boss.translate((-center_dist/2, 0, 0))

# Combine bar and bosses
result = bar.union(boss1).union(boss2)

# Create pockets on top face of each boss
result = result.faces(">Z").workplane().center(center_dist/2, 0).circle(pocket_r).cutBlind(pocket_depth)
result = result.faces(">Z").workplane().center(-center_dist/2, 0).circle(pocket_r).cutBlind(pocket_depth)