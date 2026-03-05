import cadquery as cq

# Parameters
r1_outer = 10
r1_inner = 6
r2_outer = 6
r2_inner = 3
center_dist = 60
rod_width = 6
rod_height = 5

# First ring outer solids
ring1_outer = cq.Workplane("XY").circle(r1_outer).extrude(rod_height)
ring2_outer = cq.Workplane("XY").center(center_dist, 0).circle(r2_outer).extrude(rod_height)

# Connecting rod body
rect_length = center_dist - r1_outer - r2_outer
body = (
    cq.Workplane("XY")
    .center(r1_outer + rect_length/2, 0)
    .rect(rect_length, rod_width)
    .extrude(rod_height)
)

# Union of outer shapes
combined = ring1_outer.union(ring2_outer).union(body)

# Subtract inner holes
hole1 = cq.Workplane("XY").circle(r1_inner).extrude(rod_height)
hole2 = cq.Workplane("XY").center(center_dist, 0).circle(r2_inner).extrude(rod_height)

result = combined.cut(hole1).cut(hole2)