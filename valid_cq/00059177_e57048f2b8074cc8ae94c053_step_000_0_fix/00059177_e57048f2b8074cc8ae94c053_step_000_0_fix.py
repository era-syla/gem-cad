import cadquery as cq

# Base with triangular cutout
result = (
    cq.Workplane("XZ")
    .polyline([(0, 0), (60, 0), (60, 8), (0, 8)])
    .close()
    .extrude(8)
    .cut(
        cq.Workplane("XZ")
        .polyline([(0, 8), (30, 8), (15, 0)])
        .close()
        .extrude(8)
    )
    # Add cylindrical boss/pin
    .faces(">X")
    .workplane()
    .circle(4)
    .extrude(25)
    .faces(">X")
    .workplane()
    .circle(5)
    .extrude(2)
)

# Create one slot as a box and then cut four radial slots
slot = (
    cq.Workplane("XZ")
    .center(70, 4)
    .rect(20, 2)
    .extrude(8)
)

for angle in [0, 90, 180, 270]:
    result = result.cut(
        slot.rotate((0, 4, 4), (1, 4, 4), angle)
    )