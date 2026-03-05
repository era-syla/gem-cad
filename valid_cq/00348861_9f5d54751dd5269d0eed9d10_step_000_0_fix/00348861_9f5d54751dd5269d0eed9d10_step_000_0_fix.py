import cadquery as cq

# Parameters
base_r = 35
base_h = 4
stem_r = 3
stem_h = 50

# Base
base = (
    cq.Workplane("XY")
    .circle(base_r)
    .extrude(base_h)
    .edges(">Z")
    .fillet(2)
)

# Stem
stem = (
    cq.Workplane("XY")
    .workplane(offset=base_h)
    .circle(stem_r)
    .extrude(stem_h)
    .edges(">Z")
    .fillet(1)
)

# Bowl profile (outer and inner) on XZ plane
profile = [
    (6, 0),
    (6, 2),
    (20, 20),
    (28, 38),
    (30, 40),
    (28, 40),
    (8, 3),
    (6, 1),
]

bowl = (
    cq.Workplane("XZ")
    .polyline(profile)
    .close()
    .revolve()
    .translate((0, 0, base_h + stem_h))
)

result = base.union(stem).union(bowl)