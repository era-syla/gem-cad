import cadquery as cq

# Main bracket body (top piece)
main_bracket = (
    cq.Workplane("XY")
    .box(80, 30, 12)
)

# Add notch/slot features to main bracket
main_bracket = (
    main_bracket
    .faces(">Z")
    .workplane()
    .center(30, 0)
    .rect(20, 10)
    .cutBlind(-6)
)

# Add holes to main bracket
main_bracket = (
    main_bracket
    .faces(">Z")
    .workplane()
    .pushPoints([(-25, 0), (0, 0)])
    .circle(4)
    .cutThruAll()
)

# Add side notch to main bracket
main_bracket = (
    main_bracket
    .faces(">X")
    .workplane()
    .center(0, 0)
    .rect(12, 12)
    .cutBlind(-15)
)

# Second bracket (middle piece)
second_bracket = (
    cq.Workplane("XY")
    .box(80, 30, 12)
)

second_bracket = (
    second_bracket
    .faces(">Z")
    .workplane()
    .center(30, 0)
    .rect(20, 10)
    .cutBlind(-6)
)

second_bracket = (
    second_bracket
    .faces(">Z")
    .workplane()
    .pushPoints([(-25, 0), (0, 0)])
    .circle(4)
    .cutThruAll()
)

# Third bracket (lower piece with hinge)
third_bracket = (
    cq.Workplane("XY")
    .box(80, 30, 12)
)

third_bracket = (
    third_bracket
    .faces(">Z")
    .workplane()
    .center(30, 0)
    .rect(20, 10)
    .cutBlind(-6)
)

third_bracket = (
    third_bracket
    .faces(">Z")
    .workplane()
    .pushPoints([(-25, 0), (0, 0)])
    .circle(4)
    .cutThruAll()
)

# Hinge pin on third bracket
hinge_pin = (
    cq.Workplane("XY")
    .center(45, 0)
    .cylinder(20, 6)
)

# Small anchor block (bottom left)
anchor_block = (
    cq.Workplane("XY")
    .box(40, 20, 10)
)

anchor_block = (
    anchor_block
    .faces(">Z")
    .workplane()
    .pushPoints([(-10, 0), (10, 0)])
    .circle(3)
    .cutThruAll()
)

# Wire frame arm - create as thin rectangular tubes/rods
# Rod 1 - diagonal left
rod1 = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-60, -40, 5))
    .box(3, 3, 120)
    .rotate((0,0,0),(0,1,0), 45)
)

# Assemble everything with offsets
# Position pieces
main_bracket_positioned = main_bracket.translate((0, 60, 30))
second_bracket_positioned = second_bracket.translate((0, 30, 18))
third_bracket_positioned = third_bracket.translate((0, 0, 6))
anchor_block_positioned = anchor_block.translate((-80, -60, 0))

# Create wire/arm connecting anchor to third bracket
# Use simple rod approximation
arm_wire1 = (
    cq.Workplane("XY")
    .box(3, 110, 3)
    .translate((-55, -25, 5))
    .rotate((0,0,0),(0,0,1), -30)
)

arm_wire2 = (
    cq.Workplane("XY")
    .box(3, 110, 3)
    .translate((-45, -25, 5))
    .rotate((0,0,0),(0,0,1), -25)
)

# Combine all parts
result = (
    main_bracket_positioned
    .union(second_bracket_positioned)
    .union(third_bracket_positioned)
    .union(anchor_block_positioned)
    .union(arm_wire1)
    .union(arm_wire2)
)