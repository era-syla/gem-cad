import cadquery as cq

# Base shape
base = cq.Workplane("XY").circle(20).extrude(5)

# Create fins
fin1 = cq.Workplane("YZ", origin=(0, 0, 5)).moveTo(0, 0).lineTo(25, 0).lineTo(15, 10).close().extrude(2)
fin2 = fin1.rotate((0, 0, 0), (0, 0, 1), 120)
fin3 = fin1.rotate((0, 0, 0), (0, 0, 1), 240)

# Resulting solid
result = base.union(fin1).union(fin2).union(fin3)