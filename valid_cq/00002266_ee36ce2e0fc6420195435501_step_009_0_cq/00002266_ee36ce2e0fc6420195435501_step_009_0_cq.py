import cadquery as cq

# --- Parametric Dimensions ---
# Overall plate dimensions
plate_width = 100.0   # Total width (X)
plate_length = 100.0  # Total length (Y)
thickness = 5.0       # Plate thickness (Z)

# Slot dimensions
# Large slot (on the left side)
large_slot_width = 20.0
large_slot_length = 80.0
large_slot_offset_x = -30.0 # Shifted to the left

# Small slots (on the right side)
small_slot_width = 10.0
small_slot_length = 35.0
small_slot_offset_x = 25.0  # Shifted to the right

# Vertical spacing for the two small slots
# One is shifted up, one is shifted down relative to the center
small_slot_offset_y = 25.0

# --- Modeling ---

# 1. Create the base plate
base_plate = cq.Workplane("XY").box(plate_width, plate_length, thickness)

# 2. Define the large vertical slot
# Located on the left side
large_slot = (
    cq.Workplane("XY")
    .center(large_slot_offset_x, 0)
    .rect(large_slot_width, large_slot_length)
    .extrude(thickness, both=True) # Extrude enough to cut through
)

# 3. Define the top small horizontal slot
# Located on the top right
top_small_slot = (
    cq.Workplane("XY")
    .center(small_slot_offset_x, small_slot_offset_y)
    .rect(small_slot_length, small_slot_width) # Note orientation: length is X, width is Y
    .extrude(thickness, both=True)
)

# 4. Define the bottom small horizontal slot
# Located on the bottom right
bottom_small_slot = (
    cq.Workplane("XY")
    .center(small_slot_offset_x, -small_slot_offset_y)
    .rect(small_slot_length, small_slot_width) # Note orientation: length is X, width is Y
    .extrude(thickness, both=True)
)

# 5. Combine operations: Cut slots from the base plate
result = (
    base_plate
    .cut(large_slot)
    .cut(top_small_slot)
    .cut(bottom_small_slot)
)

# Export or visualization would happen here (e.g., show_object(result))