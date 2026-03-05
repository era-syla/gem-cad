import cadquery as cq

# Parameters
R = 8
base_thickness = 4
body_height = 2 * R
base_width = 20
cylinder_length = 12
cylinder_dia = base_thickness + body_height
arch_spacing = 20
arch_count = 2
margin_end = 8

# Derived dimensions
body_length = arch_spacing * (arch_count - 1) + 2 * R + margin_end
slot_length = arch_spacing * (arch_count - 1) + 2 * R
slot_width = base_width - 4
slot_center_x = cylinder_length + R + slot_length / 2

# Create base + body block
result = cq.Workplane("XY").box(body_length, base_width, base_thickness + body_height)

# Add cylinder on the left
cyl = (
    cq.Workplane("YZ", origin=(0, 0, cylinder_dia / 2))
    .circle(cylinder_dia / 2)
    .extrude(-cylinder_length)
)
result = result.union(cyl)

# Cut out the two arch-shaped profiles
for i in range(arch_count):
    x_i = cylinder_length + R + i * arch_spacing
    arch_cut = (
        cq.Workplane("XZ", origin=(x_i, 0, base_thickness + R))
        .circle(R)
        .extrude(base_width)
    )
    result = result.cut(arch_cut)

# Cut the rectangular slot from the bottom
slot = (
    cq.Workplane("XY", origin=(slot_center_x, 0, 0))
    .rect(slot_length, slot_width)
    .extrude(-base_thickness)
)
result = result.cut(slot)