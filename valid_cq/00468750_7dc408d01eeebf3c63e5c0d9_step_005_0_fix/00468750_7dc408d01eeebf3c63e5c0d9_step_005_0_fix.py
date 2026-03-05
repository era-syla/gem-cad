import cadquery as cq

# Parameters
radius = 10
offset = radius
thickness = 5

# Start with one lobe
result = cq.Workplane("XY").circle(radius).extrude(thickness)

# Add the other three lobes at cardinal points and fuse them
for x, y in [(-offset, 0), (0, offset), (0, -offset)]:
    cyl = cq.Workplane("XY").center(x, y).circle(radius).extrude(thickness)
    result = result.union(cyl)