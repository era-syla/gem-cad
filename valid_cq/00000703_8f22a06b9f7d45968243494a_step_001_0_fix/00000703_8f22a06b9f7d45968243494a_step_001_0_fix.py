import cadquery as cq

# Main body block
main_body = (
    cq.Workplane("XY")
    .box(50, 35, 30)
)

# Left cylindrical hinge/knuckle part
hinge = (
    cq.Workplane("YZ")
    .center(0, 0)
    .workplane(offset=-25)
    .circle(14)
    .extrude(18)
)

# Combine main body with hinge
result = main_body.union(hinge.translate((-16, 0, 0)))

# Add top rail/groove features on top
# Two slots on top
result = (
    result
    .faces(">Z")
    .workplane()
    .center(5, 0)
    .rect(40, 30)
    .cutBlind(-3)
)

# Central hole through the main block (square-ish hole with rounded corners)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(8, 0)
    .rect(12, 12)
    .cutBlind(-20)
)

# Add the small bracket on the right side
bracket = (
    cq.Workplane("XY")
    .box(10, 20, 20)
    .translate((30, 0, -5))
)

result = result.union(bracket)

# Hole through the hinge cylinder
result = (
    result
    .faces("<X")
    .workplane()
    .center(0, 0)
    .circle(5)
    .cutBlind(-50)
)

# Slots on top surface (grooves between rails)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(-5, 8)
    .rect(35, 4)
    .cutBlind(-5)
)

result = (
    result
    .faces(">Z")
    .workplane()
    .center(-5, -8)
    .rect(35, 4)
    .cutBlind(-5)
)

# Small holes on the right bracket face
result = (
    result
    .faces(">X")
    .workplane()
    .center(5, 5)
    .circle(2)
    .cutBlind(-8)
)

result = (
    result
    .faces(">X")
    .workplane()
    .center(5, -5)
    .circle(2)
    .cutBlind(-8)
)

# Hole on left face (hinge hole)
result = (
    result
    .faces("<X")
    .workplane()
    .center(0, 0)
    .circle(4)
    .cutBlind(-10)
)

# Cut the slot/channel between hinge fingers
result = (
    result
    .faces(">Z")
    .workplane()
    .center(-20, 0)
    .rect(5, 6)
    .cutBlind(-15)
)

# Chamfer some edges for aesthetics
result = (
    result
    .edges("|Z")
    .chamfer(1.0)
)