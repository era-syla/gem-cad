import cadquery as cq

# Parameter definitions
plate_height = 200.0
plate_width = 50.0
plate_thickness = 5.0

# Slot parameters
slot_width = 5.0
slot_margin_top_bottom = 15.0  # Distance from top/bottom edge to slot end
slot_margin_side = 10.0        # Distance from side edge to slot center

# Calculated values
slot_length = plate_height - (2 * slot_margin_top_bottom)
slot_x_offset = (plate_width / 2.0) - slot_margin_side

# Create the model
result = (
    cq.Workplane("XY")
    # Create the base rectangular plate
    .box(plate_width, plate_height, plate_thickness)
    # Select the top face to sketch the slots
    .faces(">Z")
    .workplane()
    # Define locations for the two slots (symmetrical about Y axis)
    .pushPoints([(-slot_x_offset, 0), (slot_x_offset, 0)])
    # Create vertical slots (rotated 90 degrees)
    .slot2D(slot_length, slot_width, angle=90)
    # Cut the slots through the entire thickness
    .cutThruAll()
)