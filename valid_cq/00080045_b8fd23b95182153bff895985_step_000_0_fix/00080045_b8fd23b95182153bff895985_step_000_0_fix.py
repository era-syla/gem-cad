import cadquery as cq

# Parameters
H = 20        # total height
D = 10        # thickness (depth)
L_left = 40   # total length of left arm (including semicircle)
L_right = 20  # length of right block
R = D/2       # radius for semicircle
d1 = 6        # diameter of left hole
d2 = 10       # diameter of right hole

# Compute the length of the rectangular portion of the left arm
L_rect = L_left - R

# Right block: full height
right = cq.Workplane("XY").box(L_right, D, H, centered=(False, True, False))

# Left rectangular arm: only upper half-height, translated into place
left_rect = (
    cq.Workplane("XY")
    .box(L_rect, D, H/2, centered=(False, True, False))
    .translate((-L_rect, 0, H/2))
)

# Left semicircular end: cylinder along Y axis, extruded from XZ plane
semi_cyl = (
    cq.Workplane("XZ")
    .center(-L_rect, H/2 + R)
    .circle(R)
    .extrude(D/2, both=True)
)

# Combine solids
result = right.union(left_rect).union(semi_cyl)

# Cut left hole through thickness
result = (
    result
    .faces(">Y")
    .workplane(origin=(-L_rect / 2, H/2 + R))
    .circle(d1 / 2)
    .cutThruAll()
)

# Cut right hole through thickness
result = (
    result
    .faces(">Y")
    .workplane(origin=(L_right / 2, H/2))
    .circle(d2 / 2)
    .cutThruAll()
)