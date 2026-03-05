import cadquery as cq

# Parameters
strap_length = 200.0
strap_width = 4.0
strap_thickness = 1.0

head_length = 8.0
head_width = strap_width + 2.0
head_thickness = 3.0

ridge_pitch = 4.0
ridge_length = 2.0
ridge_height = 0.5

# Base strap
base = cq.Workplane("XY").rect(strap_width, strap_length).extrude(strap_thickness)

# Head
head = (
    cq.Workplane("XY")
    .rect(head_width, head_length)
    .extrude(head_thickness)
    .translate((0, strap_length/2 + head_length/2, 0))
)

# Combine strap and head
result = base.union(head)

# Add ridges (teeth) on top of strap
ridge_count = int(strap_length / ridge_pitch)
for i in range(ridge_count):
    y_pos = -strap_length/2 + ridge_pitch/2 + i * ridge_pitch
    ridge = (
        cq.Workplane("XY")
        .rect(strap_width, ridge_length)
        .extrude(ridge_height)
        .translate((0, y_pos, strap_thickness))
    )
    result = result.union(ridge)

# Cut slot in the head for strap insertion
slot_length = head_length - 2.0
slot = (
    cq.Workplane("XY")
    .rect(strap_width, slot_length)
    .extrude(head_thickness + 1.0)
    .translate((0, strap_length/2 + head_length/2, 0))
)
result = result.cut(slot)