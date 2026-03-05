import cadquery as cq

thickness = 5.0
outer_diameter = 80.0
inner_diameter = 70.0
bar_width = 6.0

# Outer ring
ring = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)

# Cross bars
hbar = (
    cq.Workplane("XY")
    .rect(inner_diameter, bar_width, centered=(True, True))
    .extrude(thickness)
)
vbar = (
    cq.Workplane("XY")
    .rect(bar_width, inner_diameter, centered=(True, True))
    .extrude(thickness)
)
bars = hbar.union(vbar)

# Fish silhouette (approximate)
fish_points = [
    (0, 25), (17, 17), (30, 0), (17, -17),
    (0, -20), (-12, -15), (-25, 0), (-12, 15)
]
fish = (
    cq.Workplane("XY")
    .polyline(fish_points)
    .close()
    .extrude(thickness)
)

result = ring.union(bars).union(fish)