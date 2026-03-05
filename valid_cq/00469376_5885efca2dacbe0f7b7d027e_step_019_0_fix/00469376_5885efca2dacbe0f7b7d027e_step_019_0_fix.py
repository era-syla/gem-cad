import cadquery as cq

# Parameters
radius = 50
straight = 150
thickness = 3

# Base plate with concave left edge
result = (
    cq.Workplane("XY")
    .moveTo(0, radius)
    .lineTo(straight, radius)
    .lineTo(straight, -radius)
    .lineTo(0, -radius)
    .threePointArc((-radius, 0), (0, radius))
    .close()
    .extrude(thickness)
)

# Cut rectangular slots near curved edge
slot1_positions = [(radius * 0.5, 15), (radius * 0.5, -15)]
for pos in slot1_positions:
    result = (
        result.faces(">Z")
        .workplane()
        .pushPoints([pos])
        .rect(30, 3)
        .cutThruAll()
    )

# Cut rectangular slots near straight edge
slot2_positions = [(radius + 20, 20), (radius + 20, 0), (radius + 20, -20)]
for pos in slot2_positions:
    result = (
        result.faces(">Z")
        .workplane()
        .pushPoints([pos])
        .rect(30, 3)
        .cutThruAll()
    )

# Engrave text on top face
result = (
    result.faces(">Z")
    .workplane()
    .transformed(offset=(straight * 0.4, 10, 0))
    .text("VENTOR MK2", 10, 1, cut=True)
)
result = (
    result.faces(">Z")
    .workplane()
    .transformed(offset=(straight * 0.4, -10, 0))
    .text("REV 1.0", 8, 1, cut=True)
)

# Add standoffs on bottom face
post_positions = [(40, -radius + 5), (75, -radius + 5), (110, -radius + 5)]
for pos in post_positions:
    result = (
        result.faces("<Z")
        .workplane()
        .pushPoints([pos])
        .circle(1.5)
        .extrude(-3)
    )