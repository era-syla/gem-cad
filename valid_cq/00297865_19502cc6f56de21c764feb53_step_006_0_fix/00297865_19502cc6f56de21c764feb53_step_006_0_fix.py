import cadquery as cq

# Parameters
bar_len = 200.0
bar_w = 6.0
bar_h = 6.0

flange_th = 6.0
flange_len = 20.0
flange_w = 6.0

post_w = 4.0
post_h = 40.0
post_x_offset = 50.0

rod_len = 60.0
rod_r = 1.5
rod_z_offset = bar_h/2 + rod_r

# Main beam
result = cq.Workplane("XY").box(bar_len, bar_w, bar_h)

# End flanges (small cross beams at each end, perpendicular to main beam)
for x in (bar_len/2 - flange_th/2, -bar_len/2 + flange_th/2):
    flange = (
        cq.Workplane("XY")
        .transformed(offset=(x, 0, 0))
        .box(flange_th, flange_len, flange_w)
    )
    result = result.union(flange)

# Vertical support posts underneath
for x in (post_x_offset, -post_x_offset):
    post = (
        cq.Workplane("XY")
        .transformed(offset=(x, 0, -(bar_h+post_h)/2))
        .box(post_w, post_w, post_h)
    )
    result = result.union(post)

# Cross rod on top of beam (perpendicular to main beam, along Y-axis)
rod = (
    cq.Workplane("XZ")
    .transformed(offset=(0, -rod_len/2, rod_z_offset))
    .circle(rod_r)
    .extrude(rod_len)
)
result = result.union(rod)