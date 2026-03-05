import cadquery as cq

# Parameters
thickness = 20
block_w = 20
block_h = 40
arm_l = 80
arm_h = 20
hole_d = 6
fillet_r = 2
semi_r = 10

# Create vertical support block
vertical = (
    cq.Workplane("XY")
    .box(block_w, thickness, block_h, centered=(True, True, False))
)

# Create horizontal arm
arm = (
    cq.Workplane("XY")
    .transformed(offset=(block_w/2 + arm_l/2, 0, 0))
    .box(arm_l, thickness, arm_h, centered=(True, True, False))
)

# Combine parts
result = vertical.union(arm)

# Drill holes through thickness on the front face (Y positive)
hole_positions = [
    (0, 10),                     # lower hole on vertical block
    (0, 30),                     # upper hole on vertical block
    (block_w/2 + arm_l/2, 10)    # hole on horizontal arm
]
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_d)
)

# Semi-circular pocket on front face of the arm
result = (
    result
    .faces(">Y")
    .workplane()
    .center(block_w + semi_r, arm_h/2)
    .circle(semi_r)
    .cutBlind(-thickness/2)
)

# Extrude letter "R" on the front face of the arm
result = (
    result
    .faces(">Y")
    .workplane()
    .center(block_w + arm_l/2, arm_h/2)
    .text("R", 8, 2)
)

# Fillet top edges
result = result.edges(">Z").fillet(fillet_r)