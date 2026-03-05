import cadquery as cq

# Create the base hexagon
base = cq.Workplane("XY").polygon(6, 20).extrude(2)

# Create connector cylinders
cylinders = (
    cq.Workplane("XY")
    .pushPoints([(-10, 17.32), (10, 17.32), (20, 0), (10, -17.32), (-10, -17.32), (-20, 0)])
    .circle(4)
    .extrude(8)
)

# Merge the hexagon and cylinders
result = base.union(cylinders)