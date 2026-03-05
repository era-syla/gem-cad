import cadquery as cq

# Base plate
plate = cq.Workplane("XY").rect(80, 120).extrude(3)

# Bosses
boss1 = cq.Workplane("XY").circle(4).extrude(15).translate((30, -40, 3))
boss2 = cq.Workplane("XY").circle(4).extrude(15).translate((-30, 40, 3))

# Combine parts
result = plate.union(boss1).union(boss2)