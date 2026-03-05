import cadquery as cq

# Create side walls and base of U-shaped block
left = cq.Workplane("XY").box(10, 30, 30, centered=(False, True, False))
right = cq.Workplane("XY").transformed(offset=(40, 0, 0)).box(10, 30, 30, centered=(False, True, False))
base = cq.Workplane("XY").transformed(offset=(10, 0, -10)).box(30, 30, 10, centered=(False, True, False))

body = left.union(right).union(base)

# Cut a vertical hole through the base
hole = cq.Workplane("XY").transformed(offset=(25, 0, -10)).circle(7.5).extrude(30)
body = body.cut(hole)

# Create two rods extending from the back
rod1 = cq.Workplane("XY").transformed(offset=(50, 5, 0)).circle(2.5).extrude(80)
rod2 = cq.Workplane("XY").transformed(offset=(50, -5, 0)).circle(2.5).extrude(80)

result = body.union(rod1).union(rod2)