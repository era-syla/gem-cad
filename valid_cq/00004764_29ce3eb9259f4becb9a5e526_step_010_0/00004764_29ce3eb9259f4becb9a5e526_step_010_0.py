import cadquery as cq

# Parametric dimensions
plate_length = 120.0
plate_height = 60.0
plate_thickness = 10.0

# Large slot dimensions (Left side)
large_slot_len = 40.0
large_slot_width = 18.0
large_slot_x_pos = -30.0  # Relative to plate center

# Cross pattern dimensions (Right side)
cross_center_x = 30.0     # Relative to plate center
cross_hole_dia = 6.0
small_slot_len = 16.0
small_slot_width = 8.0
small_slot_offset = 15.0  # Distance from pattern center to slot centers

# 1. Base Plate
result = cq.Workplane("XY").box(plate_length, plate_height, plate_thickness)

# 2. Large Horizontal Slot
result = (
    result.faces(">Z")
    .workplane()
    .center(large_slot_x_pos, 0)
    .slot2D(large_slot_len, large_slot_width)
    .cutThruAll()
)

# 3. Cross Pattern - Center Hole
result = (
    result.faces(">Z")
    .workplane()
    .center(cross_center_x, 0)
    .circle(cross_hole_dia / 2.0)
    .cutThruAll()
)

# 4. Cross Pattern - Horizontal Slots (Left/Right)
# Points relative to the cross center
h_points = [(-small_slot_offset, 0), (small_slot_offset, 0)]
result = (
    result.faces(">Z")
    .workplane()
    .center(cross_center_x, 0)
    .pushPoints(h_points)
    .slot2D(small_slot_len, small_slot_width, angle=0)
    .cutThruAll()
)

# 5. Cross Pattern - Vertical Slots (Top/Bottom)
# Points relative to the cross center
v_points = [(0, small_slot_offset), (0, -small_slot_offset)]
result = (
    result.faces(">Z")
    .workplane()
    .center(cross_center_x, 0)
    .pushPoints(v_points)
    .slot2D(small_slot_len, small_slot_width, angle=90)
    .cutThruAll()
)