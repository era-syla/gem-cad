import cadquery as cq

# Parameters
bar_length = 160.0
bar_height = 15.0
bar_thickness = 5.0

block_width = 24.0
block_depth = 18.0
block_height = 15.0
block_offset_x = 48.0

hole_dia = 9.0
slit_width = 1.5
screw_hole_dia = 3.5
screw_y = block_depth * 0.7

slot_offset_x = 68.0
slot_length = 6.0  # Distance between arc centers
slot_width = 4.0

# Base plane
base = cq.Workplane("XY")

# Construct the front bar (back face is aligned with Y=0)
front_bar = base.center(0, -bar_thickness / 2.0).box(bar_length, bar_thickness, bar_height)

# Construct the mounting blocks
right_block = base.center(block_offset_x, block_depth / 2.0).box(block_width, block_depth, block_height)
left_block = base.center(-block_offset_x, block_depth / 2.0).box(block_width, block_depth, block_height)

result = front_bar.union(right_block).union(left_block)

# Vertical rod holes
result = result.faces(">Z").workplane().pushPoints([
    (block_offset_x, block_depth / 2.0),
    (-block_offset_x, block_depth / 2.0)
]).hole(hole_dia)

# Clamping slits
slit = cq.Workplane("XY").pushPoints([
    (block_offset_x, block_depth * 0.75),
    (-block_offset_x, block_depth * 0.75)
]).box(slit_width, block_depth / 2.0 + 2.0, block_height + 2.0)

result = result.cut(slit)

# Clamping screw holes
screw_hole1 = cq.Workplane("YZ").workplane(offset=-block_offset_x).center(screw_y, 0).circle(screw_hole_dia / 2.0).extrude(block_width, both=True)
screw_hole2 = cq.Workplane("YZ").workplane(offset=block_offset_x).center(screw_y, 0).circle(screw_hole_dia / 2.0).extrude(block_width, both=True)

result = result.cut(screw_hole1).cut(screw_hole2)

# Mounting slots on the front bar
slots = cq.Workplane("XZ").workplane(offset=-bar_thickness/2.0).pushPoints([
    (slot_offset_x, 0),
    (-slot_offset_x, 0)
]).slot2D(slot_length, slot_width, 0).extrude(bar_thickness * 2.0, both=True)

result = result.cut(slots)