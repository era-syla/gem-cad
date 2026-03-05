import cadquery as cq

# Base plate
base = cq.Workplane("XY").box(80, 60, 6)

# Central block/pedestal on top of base
pedestal = cq.Workplane("XY").box(50, 40, 20).translate((0, 5, 13))

# Combine base and pedestal
result = base.union(pedestal)

# Two horizontal cylinders (tubes) - one lower, one upper
# Lower cylinder - horizontal along X axis
lower_cyl = cq.Workplane("YZ").circle(10).extrude(50).translate((-25, 5, 20))
# Upper cylinder - horizontal along X axis, offset up and back
upper_cyl = cq.Workplane("YZ").circle(10).extrude(50).translate((-25, 10, 36))

result = result.union(lower_cyl)
result = result.union(upper_cyl)

# Hollow out lower cylinder
lower_hole = cq.Workplane("YZ").circle(6).extrude(52).translate((-26, 5, 20))
result = result.cut(lower_hole)

# Hollow out upper cylinder
upper_hole = cq.Workplane("YZ").circle(6).extrude(52).translate((-26, 10, 36))
result = result.cut(upper_hole)

# Small square boss on left side of base with threaded hole
left_boss = cq.Workplane("XY").box(12, 12, 10).translate((-32, -18, 8))
result = result.union(left_boss)

# Hole in left boss
left_hole = cq.Workplane("XY").circle(3).extrude(12).translate((-32, -18, 4))
result = result.cut(left_hole)

# Cut notches/pockets on the sides of the pedestal to show it's raised
# Left pocket
left_pocket = cq.Workplane("XY").box(15, 40, 14).translate((-32, 5, 10))
result = result.cut(left_pocket)

# Right step cut
right_pocket = cq.Workplane("XY").box(15, 40, 14).translate((32, 5, 10))
result = result.cut(right_pocket)