import cadquery as cq

# Base disk
base = cq.Workplane("XY").circle(50).extrude(5)

# Outer ring
outer_ring = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .circle(60)
    .circle(55)
    .extrude(20)
)

# Inner support structure
inner_support = (
    cq.Workplane("XY")
    .workplane(offset=30)
    .circle(5)
    .extrude(70)
)

# Arms
arms = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .rect(5, 30, forConstruction=True)
    .vertices()
    .circle(2)
    .extrude(15)
    .rotate((0, 0, 0), (0, 0, 1), 90)
)

# Combine all parts
result = base.union(outer_ring).union(inner_support).union(arms)