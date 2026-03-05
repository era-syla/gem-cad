import cadquery as cq

# Create base sketch
base = cq.Workplane("XY").rect(40, 10).extrude(5)

# Create central cylinder
cylinder1 = cq.Workplane("XY").workplane(offset=5).circle(10).extrude(10)

# Create smaller cylinder
cylinder2 = cq.Workplane("XY").workplane(offset=5).circle(5).extrude(5)

# Combine shapes
combined = base.union(cylinder1).union(cylinder2)

# Create cutout
slot = (
    cq.Workplane("XY")
    .workplane(offset=5)
    .center(0, 0)
    .slot2D(25, 3, angle=0)
    .extrude(5)
)

# Subtract slot from the base
result = combined.cut(slot)