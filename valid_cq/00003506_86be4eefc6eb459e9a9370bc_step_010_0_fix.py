import cadquery as cq

# Main telescope/scope body - cylinder
body_length = 80
body_radius = 15
front_radius = 18
front_length = 8

# Main tube body
main_body = (
    cq.Workplane("YZ")
    .circle(body_radius)
    .extrude(body_length)
)

# Front flange/bell
front_flange = (
    cq.Workplane("YZ")
    .circle(front_radius)
    .extrude(front_length)
)

# Combine body and front flange
scope = main_body.union(front_flange)

# Hollow out the tube
scope = (
    scope
    .faces(">X")
    .workplane()
    .circle(body_radius - 2)
    .cutBlind(-body_length + 5)
)

# Hollow front opening
scope = (
    scope
    .faces("<X")
    .workplane()
    .circle(front_radius - 2)
    .cutBlind(-front_length - 2)
)

# Add threaded/knurled section near back - represented as slightly larger cylinder rings
# Adjustment ring near back
adj_ring = (
    cq.Workplane("YZ")
    .transformed(offset=(0, 0, 60))
    .circle(body_radius + 1.5)
    .extrude(12)
)

scope = scope.union(adj_ring)

# Side knob/adjustment screw - small cylinder sticking out from the side
knob_stem = (
    cq.Workplane("XZ")
    .transformed(offset=(66, 0, -(body_radius + 8)))
    .circle(2.5)
    .extrude(12)
)

knob_head = (
    cq.Workplane("XZ")
    .transformed(offset=(66, 0, -(body_radius + 20)))
    .circle(6)
    .extrude(5)
)

scope = scope.union(knob_stem).union(knob_head)

# Bottom mount/support - two small cylindrical feet at the bottom
foot1 = (
    cq.Workplane("XY")
    .transformed(offset=(10, -(body_radius + 5), 0))
    .circle(4)
    .extrude(5)
)

foot_base1 = (
    cq.Workplane("XY")
    .transformed(offset=(10, -(body_radius + 8), 0))
    .circle(7)
    .extrude(3)
)

scope = scope.union(foot1).union(foot_base1)

# Second foot
foot2 = (
    cq.Workplane("XY")
    .transformed(offset=(65, -(body_radius + 5), 0))
    .circle(4)
    .extrude(5)
)

foot_base2 = (
    cq.Workplane("XY")
    .transformed(offset=(65, -(body_radius + 8), 0))
    .circle(7)
    .extrude(3)
)

scope = scope.union(foot2).union(foot_base2)

# Small bolt/screw on front face
bolt1 = (
    cq.Workplane("YZ")
    .transformed(offset=(0, front_radius - 4, 3))
    .circle(1.5)
    .extrude(3)
)

scope = scope.union(bolt1)

# Add small side bump near front
side_bump = (
    cq.Workplane("XZ")
    .transformed(offset=(5, 0, -(front_radius - 1)))
    .circle(3)
    .extrude(4)
)

scope = scope.union(side_bump)

result = scope