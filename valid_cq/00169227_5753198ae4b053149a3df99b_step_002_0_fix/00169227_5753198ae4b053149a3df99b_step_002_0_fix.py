import cadquery as cq

# Parameters
R_big = 20.0        # outer radius of the central clamp
R_small = 8.0       # outer radius of the end clamps
connector = 6.0     # gap between central and end clamps
thickness = 5.0     # thickness of the part
t_big = 2.0         # wall thickness of central clamp
t_small = 2.0       # wall thickness of end clamps

# Derived distances
b = R_big + connector                   # half‐length of the center bar
small_center = b + R_small              # x-position of small clamp centers
cyl_center = small_center + R_small     # x-position for the half‐cylinder cuts

# Build the main bar
result = cq.Workplane("XY").rect(2*b, 2*R_small).extrude(thickness)

# Add the big clamp bulge
result = result.union(
    cq.Workplane("XY").circle(R_big).extrude(thickness)
)

# Add the two small clamp bulges
for x in (small_center, -small_center):
    result = result.union(
        cq.Workplane("XY")
        .transformed(offset=(x, 0, 0))
        .circle(R_small)
        .extrude(thickness)
    )

# Cut out the central through‐hole
inner_big = R_big - t_big
result = result.cut(
    cq.Workplane("XY").circle(inner_big).extrude(thickness)
)

# Cut out the two half‐cylinder end holes
inner_small = R_small - t_small
for x in (cyl_center, -cyl_center):
    result = result.cut(
        cq.Workplane("XY")
        .transformed(offset=(x, 0, 0))
        .circle(inner_small)
        .extrude(thickness)
    )