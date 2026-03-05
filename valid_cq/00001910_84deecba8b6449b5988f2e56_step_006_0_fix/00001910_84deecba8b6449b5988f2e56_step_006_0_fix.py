import cadquery as cq

# Parameters
r_base = 20
h_base = 4
r_riser = 10
h_riser = 5
h_body = 42
r_mid = 25
h_top_riser = 5
h_top_disc = 4
r_hole = 5

# Compute z-levels
z0 = 0
z1 = z0 + h_base
z2 = z1
z3 = z2 + h_riser
z4 = z3 + h_body / 2
z5 = z3 + h_body
z6 = z5 + h_top_riser
z7 = z6 + h_top_disc

# Define profile points in the X-Z plane
p0 = (r_base, z0)
p1 = (r_base, z1)
p2 = (r_riser, z2)
p3 = (r_riser, z3)
p4 = (r_mid,   z4)
p5 = (r_riser, z5)
p6 = (r_riser, z6)
p6_out = (r_base, z6)
p7 = (r_base, z7)

# Build the outer profile and revolve
wp = (
    cq.Workplane("XZ")
    .moveTo(*p0)
    .lineTo(*p1)
    .lineTo(*p2)
    .lineTo(*p3)
    .threePointArc(p4, p5)
    .lineTo(*p6)
    .lineTo(*p6_out)
    .lineTo(*p7)
    .lineTo(0, z7)
    .close()
)

result = wp.revolve(360, axisStart=(0, 0, 0), axisEnd=(0, 0, 1))

# Cut the top hole
hole = (
    cq.Workplane("XY")
    .workplane(offset=z6)
    .circle(r_hole)
    .extrude(h_top_disc)
)
result = result.cut(hole)