import cadquery as cq

# Dimensions
plate_length = 100.0
plate_width = 60.0
plate_thickness = 5.0

slot_length = 70.0
slot_width = 12.0
slot_offset_y = 15.0  # Distance from the center of the plate to the center of the slot

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z")
    .workplane()
    .center(0, slot_offset_y)
    .rect(slot_length, slot_width)
    .cutThruAll()
)