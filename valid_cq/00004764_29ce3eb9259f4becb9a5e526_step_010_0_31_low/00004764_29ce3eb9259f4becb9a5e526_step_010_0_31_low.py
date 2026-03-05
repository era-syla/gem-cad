import cadquery as cq

# Parameters
length = 100.0
height = 40.0
thickness = 5.0

large_slot_length = 20.0
large_slot_width = 10.0
large_slot_x = -20.0
large_slot_y = -5.0

small_slot_length = 10.0
small_slot_width = 5.0
slot_pattern_radius = 12.0

# Base plate
base = cq.Workplane("XY").box(length, height, thickness)

# Large slot
result = (
    base.faces(">Z").workplane()
    .center(large_slot_x, large_slot_y)
    .slot2D(large_slot_length, large_slot_width)
    .cutThruAll()
)

# Small slots pattern
pattern_center_x = 20.0
pattern_center_y = 5.0

result = (
    result.faces(">Z").workplane()
    .center(pattern_center_x, pattern_center_y)
    .pushPoints([(0, slot_pattern_radius), (0, -slot_pattern_radius)])
    .slot2D(small_slot_length, small_slot_width, angle=90)
    .cutThruAll()
)

result = (
    result.faces(">Z").workplane()
    .center(pattern_center_x, pattern_center_y)
    .pushPoints([(slot_pattern_radius, 0), (-slot_pattern_radius, 0)])
    .slot2D(small_slot_length, small_slot_width, angle=0)
    .cutThruAll()
)