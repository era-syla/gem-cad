import cadquery as cq

# Base shape
base = cq.Workplane("XY").box(40, 5, 5)

# Arm extension
arm = base.faces("<Z").workplane().transformed(offset=(0, 0, 3), rotate=(45, 0, 0)).rect(5, 20).extrude(15)

# Gear creation
gear = cq.Workplane("XY").center(22.5, 0).polygon(nSides=7, diameter=20).extrude(5)

# Combine all parts
result = arm.union(gear).combine()