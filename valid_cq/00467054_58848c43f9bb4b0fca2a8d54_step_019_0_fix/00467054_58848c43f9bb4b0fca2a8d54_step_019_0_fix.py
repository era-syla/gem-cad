import cadquery as cq

# Main body
body = (
    cq.Workplane("XY")
    .rect(60, 120)
    .extrude(20)
    .edges("|Z")
    .fillet(5)
)

# Arm template
arm = (
    cq.Workplane("XY")
    .polygon(6, 15)
    .extrude(40)
    .faces(">Z")
    .workplane()
    .hole(8)
)

# Rotate and position arms
arm_positions = [
    ((-60, 30, 20), 45),
    ((60, 30, 20), -45),
    ((-60, -30, 20), 135),
    ((60, -30, 20), -135),
]

arms = cq.Workplane("XY")
for pos, angle in arm_positions:
    arms = arms.union(
        arm.translate(pos).rotate((0, 0, 0), (0, 0, 1), angle)
    )

# Combine body and arms
result = body.union(arms)