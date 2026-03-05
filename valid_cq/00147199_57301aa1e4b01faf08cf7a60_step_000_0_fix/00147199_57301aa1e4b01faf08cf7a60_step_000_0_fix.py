import cadquery as cq

# Dimensions for the main plate
plate_thickness = 5.0
plate_width = 100.0
plate_height = 100.0

# Dimensions for slots and holes
slot_length = 20.0
slot_width = 5.0
slot_offset = 15.0
hole_diameter = 5.0
hole_offset = 10.0

# Create the main plate
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# Create slots
slot = cq.Workplane("XY").slot2D(slot_length, slot_width).extrude(plate_thickness)
result = result.cut(slot.translate((slot_offset, slot_offset, 0))) \
               .cut(slot.translate((-slot_offset, slot_offset, 0))) \
               .cut(slot.translate((slot_offset, -slot_offset, 0))) \
               .cut(slot.translate((-slot_offset, -slot_offset, 0)))

# Create holes
hole = cq.Workplane("XY").circle(hole_diameter / 2).extrude(plate_thickness)
result = result.cut(hole.translate((0, 0, 0))) \
               .cut(hole.translate((hole_offset, hole_offset, 0))) \
               .cut(hole.translate((-hole_offset, hole_offset, 0))) \
               .cut(hole.translate((hole_offset, -hole_offset, 0))) \
               .cut(hole.translate((-hole_offset, -hole_offset, 0)))