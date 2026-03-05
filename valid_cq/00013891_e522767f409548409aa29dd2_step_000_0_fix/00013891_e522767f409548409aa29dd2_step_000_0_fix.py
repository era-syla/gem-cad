import cadquery as cq

# Parameters
length = 150.0
width = 30.0
height = 20.0
wall_thk = 2.0
back_solid = 15.0
rail_thk = 3.0
rail_height = 2.0

# Main body: a solid box
result = cq.Workplane("XY").box(length, width, height)

# Internal slot: a rectangular pocket from the front face
slot_length = length - back_solid
slot_width = width - 2 * wall_thk
slot_depth = height - wall_thk  # leave top wall_thk thickness
slot_center = (
    -length / 2 + slot_length / 2,
    0,
    -height / 2 + slot_depth / 2,
)
slot = (
    cq.Workplane("XY")
    .transformed(offset=slot_center)
    .box(slot_length, slot_width, slot_depth)
)
result = result.cut(slot)

# Side rails inside the slot
rail_center_x = slot_center[0]
rail_center_z = -height / 2 + rail_height / 2
rail_offset_y = width / 2 - wall_thk - rail_thk / 2

rail1 = (
    cq.Workplane("XY")
    .transformed(offset=(rail_center_x, rail_offset_y, rail_center_z))
    .box(slot_length, rail_thk, rail_height)
)
rail2 = (
    cq.Workplane("XY")
    .transformed(offset=(rail_center_x, -rail_offset_y, rail_center_z))
    .box(slot_length, rail_thk, rail_height)
)

result = result.union(rail1).union(rail2)