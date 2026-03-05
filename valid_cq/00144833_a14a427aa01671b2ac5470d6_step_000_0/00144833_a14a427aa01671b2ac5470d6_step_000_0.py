import cadquery as cq

# -- Geometric Parameters --
plate_length = 100.0
plate_height = 50.0
plate_thickness = 5.0

# Feature Dimensions
slot_width = 5.0            # Width (diameter) of the slot cuts
h_slot_length = 50.0        # Total length of horizontal slots
v_slot_length = 30.0        # Total length of vertical slot

# Feature Positioning
# Assuming origin is at the center of the plate
h_slot_x_center = -15.0     # Horizontal slots shifted to the left
h_slot_y_offset = 12.5      # Distance from center line for horizontal slots
v_slot_x_center = 35.0      # Vertical slot shifted to the right

# -- Model Construction --

# 1. Create the base rectangular plate
result = cq.Workplane("XY").box(plate_length, plate_height, plate_thickness)

# 2. Cut the two horizontal slots
# We select the top face, push two points for the centers, and cut the slots
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (h_slot_x_center, h_slot_y_offset), 
        (h_slot_x_center, -h_slot_y_offset)
    ])
    .slot2D(length=h_slot_length, diameter=slot_width, angle=0)
    .cutThruAll()
)

# 3. Cut the single vertical slot
# We push the center point for the vertical slot and cut at 90 degrees
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(v_slot_x_center, 0)])
    .slot2D(length=v_slot_length, diameter=slot_width, angle=90)
    .cutThruAll()
)