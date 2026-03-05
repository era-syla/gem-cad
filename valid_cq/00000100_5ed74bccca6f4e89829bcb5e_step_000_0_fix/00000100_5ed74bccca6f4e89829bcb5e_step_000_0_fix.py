import cadquery as cq

# Drawing compass - simplified 3D model
# Main components: hinge at top, two legs extending down

# Hinge/head assembly at top
hinge = (
    cq.Workplane("XY")
    .circle(8)
    .extrude(6)
)

# Central knob on hinge
knob = (
    cq.Workplane("XY")
    .workplane(offset=6)
    .circle(4)
    .extrude(4)
)

# Decorative wing/ear shapes on hinge
wing_left = (
    cq.Workplane("XZ")
    .center(-10, 6)
    .ellipse(6, 10)
    .extrude(3)
)

wing_right = (
    cq.Workplane("XZ")
    .center(10, 6)
    .ellipse(6, 10)
    .extrude(3)
)

# Left leg (pencil/pen side) - angled
left_leg = (
    cq.Workplane("XY")
    .center(-3, 0)
    .rect(4, 80)
    .extrude(3)
)

# Right leg (needle/point side) - angled
right_leg = (
    cq.Workplane("XY")
    .center(3, 0)
    .rect(4, 75)
    .extrude(3)
)

# Rotate legs to form V shape
left_leg_rotated = left_leg.rotate((0, 0, 0), (0, 0, 1), 15)
right_leg_rotated = right_leg.rotate((0, 0, 0), (0, 0, 1), -15)

# Pencil holder cup at bottom of left leg
pencil_cup = (
    cq.Workplane("XY")
    .center(-22, -60)
    .circle(6)
    .extrude(15)
)

pencil_cup_inner = (
    cq.Workplane("XY")
    .center(-22, -60)
    .circle(4.5)
    .extrude(12)
)

pencil_cup = pencil_cup.cut(pencil_cup_inner)

# Needle point at bottom of right leg
needle = (
    cq.Workplane("XY")
    .center(22, -60)
    .circle(2)
    .extrude(2)
)

needle_tip = (
    cq.Workplane("XY")
    .center(22, -62)
    .circle(2)
    .workplane(offset=-10)
    .circle(0.3)
    .loft()
)

# Adjustment screw bar between legs (middle section)
screw_bar = (
    cq.Workplane("XY")
    .center(0, -25)
    .rect(3, 20)
    .extrude(3)
)

# Assemble all parts
result = (
    hinge
    .union(knob)
    .union(wing_left)
    .union(wing_right)
    .union(left_leg_rotated)
    .union(right_leg_rotated)
    .union(pencil_cup)
    .union(needle)
    .union(needle_tip)
    .union(screw_bar)
)