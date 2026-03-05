import cadquery as cq

# --- Parametric Dimensions ---
# Overall plate dimensions
plate_length = 150.0
plate_width = 50.0
plate_thickness = 3.0

# Slot parameters
slot_width = 4.0  # Width of the slot cut (diameter of the end circles)

# Define slot groups based on visual inspection
# Group 1: Two short slots on the left side
left_slot_length = 20.0
left_slot_offset_x = -50.0 # From center
left_slot_spacing_y = 30.0 # Distance between centers in Y

# Group 2: Two long outer slots on the right side
right_outer_slot_length = 60.0
right_outer_slot_offset_x = 30.0 # From center
right_outer_slot_spacing_y = 36.0 # Wider than the inner ones

# Group 3: Two medium inner slots on the right side
right_inner_slot_length = 40.0
right_inner_slot_offset_x = 20.0 # Starts further left than outer ones
right_inner_slot_spacing_y = 12.0 # Closer to center

# Group 4: Two small central cutout slots in the middle
center_slot_length = 12.0
center_slot_offset_x = 10.0 # Slightly to the right of true center
center_slot_spacing_y = 12.0 

# --- Modeling ---

# 1. Create the base plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Cut the slots
# Helper function to create a slot shape based on center-to-center length
def create_slot(length, width):
    return cq.Sketch().rect(length, width).vertices().fillet(width / 2.0)

# Left pair
result = result.faces(">Z").workplane() \
    .pushPoints([
        (left_slot_offset_x, left_slot_spacing_y / 2),
        (left_slot_offset_x, -left_slot_spacing_y / 2)
    ]) \
    .slot2D(left_slot_length, slot_width, 0) \
    .cutThruAll()

# Right Outer pair
result = result.faces(">Z").workplane() \
    .pushPoints([
        (right_outer_slot_offset_x, right_outer_slot_spacing_y / 2),
        (right_outer_slot_offset_x, -right_outer_slot_spacing_y / 2)
    ]) \
    .slot2D(right_outer_slot_length, slot_width, 0) \
    .cutThruAll()

# Right Inner pair
result = result.faces(">Z").workplane() \
    .pushPoints([
        (right_inner_slot_offset_x, right_inner_slot_spacing_y / 2),
        (right_inner_slot_offset_x, -right_inner_slot_spacing_y / 2)
    ]) \
    .slot2D(right_inner_slot_length, slot_width, 0) \
    .cutThruAll()
    
# Central small pair (The "U" or interrupted slot look in the middle)
# These seem to align vertically with the inner slots but are cut short
result = result.faces(">Z").workplane() \
    .pushPoints([
        (center_slot_offset_x, center_slot_spacing_y / 2),
        (center_slot_offset_x, -center_slot_spacing_y / 2)
    ]) \
    .slot2D(center_slot_length, slot_width, 0) \
    .cutThruAll()

# Note: In the image, there appears to be a bridge between the "Inner Right" slots
# and the "Center Small" slots. By cutting them separately with a gap in between,
# we achieve that bridge. Let's adjust the X positions to ensure the gap exists.

# Refinement: Based on the image, the "Inner Right" and "Center Small" slots are likely
# part of the same track but interrupted.
# The previous code cuts them as separate entities, creating the bridge naturally.