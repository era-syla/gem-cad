import cadquery as cq

# Create a figure-8 / pill-shaped base plate
# The shape looks like two overlapping circles forming an elongated oval/peanut shape

# Parameters
large_r = 45  # larger circle radius
small_r = 30  # smaller circle radius
thickness = 4  # plate thickness
center_dist = 40  # distance between circle centers

# Create the base shape using two circles united
large_circle = cq.Workplane("XY").circle(large_r)
small_circle = cq.Workplane("XY").center(-center_dist, 0).circle(small_r)

# Build base plate using union of two cylinders
base_large = cq.Workplane("XY").cylinder(thickness, large_r)
base_small = cq.Workplane("XY").center(-center_dist, 0).cylinder(thickness, small_r)

base = base_large.union(base_small)

# Add slight chamfer/fillet to the edges
base = base.edges("|Z").fillet(3)
base = base.edges(">Z").chamfer(0.5)

# Add mounting bosses (small cylindrical bumps) at corners
boss_h = 3
boss_r = 4
boss_inner_r = 2

# Boss positions - 4 bosses around the plate
boss_positions = [
    (30, 25),
    (30, -25),
    (-50, 18),
    (-50, -18),
]

for bx, by in boss_positions:
    boss = cq.Workplane("XY").center(bx, by).cylinder(thickness + boss_h, boss_r)
    base = base.union(boss)

# Add screw holes through bosses
for bx, by in boss_positions:
    hole = cq.Workplane("XY").center(bx, by).cylinder(thickness + boss_h + 2, boss_inner_r)
    base = base.cut(hole)

# Add a raised inner profile area (the organic shape in the middle)
# Approximate with an ellipse-like raised area
inner_raise = (cq.Workplane("XY")
               .center(5, 0)
               .ellipse(25, 18)
               .extrude(1.5))

base = base.union(inner_raise)

# Add a small rectangular slot/feature
slot = (cq.Workplane("XY")
        .center(-10, 0)
        .rect(15, 3)
        .extrude(thickness + 2))

base = base.cut(slot)

# Add small tabs/clips on the sides
tab_positions = [(-center_dist - small_r + 2, 0), (large_r - 2, 0)]
for tx, ty in tab_positions:
    tab = (cq.Workplane("XY")
           .center(tx, ty)
           .rect(4, 10)
           .extrude(thickness + 1))
    base = base.union(tab)

result = base