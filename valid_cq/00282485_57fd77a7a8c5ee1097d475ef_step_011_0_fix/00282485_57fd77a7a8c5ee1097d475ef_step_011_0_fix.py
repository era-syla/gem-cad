import cadquery as cq

# Create the main cylindrical body
shaft = cq.Workplane("XY").circle(5).extrude(20)

# Create the head of the screw
head = (
    cq.Workplane("XY")
    .workplane(offset=20)
    .circle(8)
    .extrude(3)
    .edges(">Z")
    .fillet(2)
)

# Create the slot of the screw head
slot_1 = (
    cq.Workplane("XY")
    .workplane(offset=23)
    .rect(8, 1)
    .extrude(-1)
)

slot_2 = (
    cq.Workplane("XY")
    .workplane(offset=23)
    .rect(1, 8)
    .extrude(-1)
)

# Combine slots with the head
head_with_slot = head.cut(slot_1).cut(slot_2)

# Combine head and shaft
result = shaft.union(head_with_slot)