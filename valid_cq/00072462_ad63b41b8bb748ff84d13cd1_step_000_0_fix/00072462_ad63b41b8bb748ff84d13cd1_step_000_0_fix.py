import cadquery as cq

# Create the microphone head
head = (
    cq.Workplane("XY")
    .box(60, 40, 80)
    .edges("|Z")
    .fillet(8)
)

# Cut horizontal slots on the top face
model = head
slot_length = 36
slot_width = 2
num_slots = 10
spacing = 6

for i in range(num_slots):
    x = -((num_slots - 1) * spacing) / 2 + i * spacing
    model = (
        model.faces(">Z")
        .workplane()
        .transformed(offset=(x, 0, 0))
        .rect(slot_length, slot_width)
        .cutBlind(-82)
    )

# Create the handle
handle = (
    cq.Workplane("XY")
    .workplane(offset=-40)
    .circle(5)
    .extrude(-100)
)

# Combine head and handle
result = model.union(handle)