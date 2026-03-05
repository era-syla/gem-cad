import cadquery as cq

# Parameters
inner_r = 20
outer_r = 40
height = 10
fillet_r = 2

# Create a full ring
ring = (
    cq.Workplane("XY")
    .circle(outer_r)
    .circle(inner_r)
    .extrude(height)
)

# Cut away the negative-X half
cut_x = (
    cq.Workplane("XY")
    .box(inner_r + outer_r, 2 * outer_r, 2 * height)
    .translate((-(inner_r + outer_r) / 2, 0, height / 2))
)

# Cut away the negative-Y half
cut_y = (
    cq.Workplane("XY")
    .box(2 * outer_r, inner_r + outer_r, 2 * height)
    .translate((0, -(inner_r + outer_r) / 2, height / 2))
)

# Apply cuts to get a 90° segment
segment = ring.cut(cut_x).cut(cut_y)

# Fillet the top edges
result = segment.faces(">Z").edges().fillet(fillet_r)