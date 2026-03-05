import cadquery as cq

# Main vertical strap/bar
strap = (
    cq.Workplane("XY")
    .rect(8, 120)
    .extrude(3)
)

# Hole at bottom of strap
strap = (
    strap
    .faces(">Z")
    .workplane()
    .center(0, -52)
    .circle(4)
    .cutThruAll()
)

# Main body/block in upper portion
block = (
    cq.Workplane("XY")
    .center(0, 30)
    .rect(18, 22)
    .extrude(18)
)

# Combine strap and block
result = strap.union(block)

# Top bracket plate (horizontal cross piece)
top_plate = (
    cq.Workplane("XY")
    .center(0, 46)
    .rect(30, 8)
    .extrude(12)
)

result = result.union(top_plate)

# Small tab at top of bracket
top_tab = (
    cq.Workplane("XY")
    .center(0, 52)
    .rect(14, 4)
    .extrude(18)
)

result = result.union(top_tab)

# Left wing of bracket
left_wing = (
    cq.Workplane("XY")
    .center(-18, 42)
    .rect(8, 10)
    .extrude(8)
)

result = result.union(left_wing)

# Right wing of bracket
right_wing = (
    cq.Workplane("XY")
    .center(18, 42)
    .rect(8, 10)
    .extrude(8)
)

result = result.union(right_wing)

# Cut slot/groove in block face
result = (
    result
    .faces(">X")
    .workplane()
    .center(0, 0)
    .rect(2, 18)
    .cutBlind(-4)
)

# Add small detail cuts on block
result = (
    result
    .faces(">X")
    .workplane()
    .center(0, 4)
    .rect(1.5, 1.5)
    .cutBlind(-2)
)

result = (
    result
    .faces(">X")
    .workplane()
    .center(0, 0)
    .rect(1.5, 1.5)
    .cutBlind(-2)
)

result = (
    result
    .faces(">X")
    .workplane()
    .center(0, -4)
    .rect(1.5, 1.5)
    .cutBlind(-2)
)