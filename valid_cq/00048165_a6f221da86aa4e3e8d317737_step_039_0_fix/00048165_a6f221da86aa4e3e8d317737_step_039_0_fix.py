import cadquery as cq

# Create base ring: lower flange and upper ring
base1 = cq.Workplane("XY").circle(32).circle(20).extrude(1)
base2 = (
    cq.Workplane("XY")
    .circle(30)
    .circle(20)
    .extrude(5)
    .translate((0, 0, 1))
)
ring = base1.union(base2)

# Create and add lower external teeth (24 teeth)
teeth = None
for i in range(24):
    tooth = (
        cq.Workplane("XY")
        .polyline([(32, 0), (34, 0), (34, 1), (32, 1)])
        .close()
        .extrude(1)
        .rotate((0, 0, 0), (0, 0, 1), i * 360 / 24)
    )
    teeth = tooth if teeth is None else teeth.union(tooth)

# Create inner radial slots (8 slots) on the upper ring
slots = None
for j in range(8):
    slot = (
        cq.Workplane("XY")
        .polyline([(18, 0), (20, 0), (20, 4), (18, 4)])
        .close()
        .extrude(4)
        .translate((0, 0, 1))
        .rotate((0, 0, 0), (0, 0, 1), j * 360 / 8)
    )
    slots = slot if slots is None else slots.union(slot)

# Combine everything
result = ring.union(teeth).cut(slots)