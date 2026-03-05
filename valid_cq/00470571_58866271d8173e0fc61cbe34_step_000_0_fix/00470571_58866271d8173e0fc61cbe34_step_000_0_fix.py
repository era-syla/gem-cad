import cadquery as cq

# Parameters
R = 25.0
base_thick = 8.0
ext_left = 20.0
length = 40.0
ext_right = 20.0
total_length = ext_left + length + ext_right
width = 2 * R + 2 * base_thick
side_wall_thickness = base_thick
side_wall_height = R
slot_width = 12.0
side_block_width = 2 * side_wall_thickness + slot_width
hole_dia = 6.0
hole_spacing_y = width / 3

# Base block
result = cq.Workplane("XY").box(total_length, width, base_thick)

# Top half‐cylinder
cyl = cq.Workplane("YZ").workplane(offset=ext_left).circle(R).extrude(length)
result = result.union(cyl)

# Side block with slot
side_block = (
    cq.Workplane("XY")
    .workplane(offset=base_thick)
    .transformed(offset=(ext_left + length + ext_right / 2, 0, 0))
    .box(ext_right, side_block_width, side_wall_height)
)
result = result.union(side_block)
slot_cut = (
    cq.Workplane("XY")
    .workplane(offset=base_thick)
    .transformed(offset=(ext_left + length + ext_right / 2, 0, 0))
    .box(ext_right + 1, slot_width, side_wall_height + 1)
)
result = result.cut(slot_cut)

# Inner groove for pipe
inner_cyl = (
    cq.Workplane("YZ")
    .workplane(offset=ext_left)
    .circle(R)
    .extrude(length)
    .translate((0, 0, base_thick))
)
result = result.cut(inner_cyl)

# Holes on left flange
x_hole = -total_length / 2 + ext_left / 2
y1 = hole_spacing_y / 2
y2 = -hole_spacing_y / 2
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(x_hole, y1), (x_hole, y2)])
    .hole(hole_dia, base_thick + 1)
)

# Center hole on cylinder
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 0)])
    .hole(hole_dia, R + base_thick + 1)
)