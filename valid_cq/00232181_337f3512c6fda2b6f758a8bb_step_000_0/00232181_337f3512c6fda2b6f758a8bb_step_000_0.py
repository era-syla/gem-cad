import cadquery as cq

# --- Dimensions & Parameters ---
# Main Plate
plate_length = 280.0
plate_width = 140.0
plate_thickness = 3.0
corner_fillet = 10.0

# Central Hole Pattern
grid_rows = 7
grid_cols = 7
grid_pitch = 8.0
hole_diameter = 4.0

# Side Dashed Slots
slot_length = 18.0
slot_width = 3.5
slot_spacing_x = 26.0  # Center-to-center spacing along X
slot_group_start_x = 65.0  # X position of the first slot center from origin
slot_row_offset_y = 38.0   # Y position of the slot rows from origin

# Handle
handle_length = 60.0
handle_width = 12.0
handle_offset_y = -50.0

# --- Modeling ---

# 1. Create the base plate with rounded corners
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .fillet(corner_fillet)
)

# 2. Create the central grid of holes
# rarray creates a grid of points, circle creates the profile, cutThruAll removes material
result = (
    result.faces(">Z")
    .workplane()
    .rarray(grid_pitch, grid_pitch, grid_cols, grid_rows)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# 3. Create the side slots (dashed lines)
# Calculate positions for the 4 groups of slots (Top-Left, Bottom-Left, Top-Right, Bottom-Right)
slot_points = []
num_slots_per_row = 3

for i in range(num_slots_per_row):
    # Calculate X coordinate for the current slot in the sequence
    x_pos = slot_group_start_x + (i * slot_spacing_x)
    
    # Add points for all four quadrants based on symmetry
    slot_points.append((x_pos, slot_row_offset_y))   # Top-Right
    slot_points.append((x_pos, -slot_row_offset_y))  # Bottom-Right
    slot_points.append((-x_pos, slot_row_offset_y))  # Top-Left
    slot_points.append((-x_pos, -slot_row_offset_y)) # Bottom-Left

# slot2D requires the length between arc centers
slot_c2c_length = slot_length - slot_width

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(slot_points)
    .slot2D(slot_c2c_length, slot_width, 0)
    .cutThruAll()
)

# 4. Create the handle slot
handle_c2c_length = handle_length - handle_width

result = (
    result.faces(">Z")
    .workplane()
    .center(0, handle_offset_y)
    .slot2D(handle_c2c_length, handle_width, 0)
    .cutThruAll()
)