import cadquery as cq

# --- Parameters ---
# Overall dimensions
plate_width = 200.0   # Total width of the plate (X axis)
plate_depth = 200.0   # Total depth of the plate (Y axis)
plate_height = 10.0   # Thickness of the plate (Z axis)

# T-Slot parameters (T-slot profile)
# The T-slot consists of a narrow upper channel and a wider lower channel
# Dimensions estimated for a common M5 or M6 T-slot size relative to a 200mm plate
slot_top_w = 6.0      # Width of the opening at the top
slot_bottom_w = 10.0  # Width of the wider bottom section
slot_top_h = 3.0      # Depth of the narrow top section
slot_bottom_h = 3.0   # Height of the wider bottom section
slot_total_h = slot_top_h + slot_bottom_h

# Grid parameters
grid_pitch_x = 20.0   # Distance between slots in X direction
grid_pitch_y = 20.0   # Distance between slots in Y direction

# Calculate number of slots
# We want them centered.
num_slots_x = int(plate_width // grid_pitch_x)
num_slots_y = int(plate_depth // grid_pitch_y)

# --- Geometry Construction ---

# 1. Create the base plate
base = cq.Workplane("XY").box(plate_width, plate_depth, plate_height)

# 2. Define the T-slot cutting profile 
# We will sketch the cross-section of the T-slot and extrude/cut it.
# The sketch is on the XZ or YZ plane depending on the slot direction.

def create_t_slot_profile():
    """Returns a sketch of the T-slot inverted for subtraction"""
    return (cq.Sketch()
            .rect(slot_bottom_w, slot_bottom_h)  # Bottom wide part
            .push([(0, (slot_bottom_h + slot_top_h)/2)])
            .rect(slot_top_w, slot_top_h + slot_bottom_h) # Top narrow part (overlapping)
            # We need to position this relative to the top surface
            # The logic below handles the positioning during cut
            )

# Since CadQuery cuts are often easier with simple shapes or specific profile extrusions,
# let's try a different approach: constructing the cut solid for one slot and patterning it.

# Profile for the T-slot cut
# We draw the T shape centered on Y axis, oriented on XZ plane (for slots running along Y)
# Coordinate system: Origin at the top surface level
t_profile = (
    cq.Workplane("XZ")
    .moveTo(-slot_top_w/2, 0)
    .lineTo(-slot_top_w/2, -slot_top_h)
    .lineTo(-slot_bottom_w/2, -slot_top_h)
    .lineTo(-slot_bottom_w/2, -slot_total_h)
    .lineTo(slot_bottom_w/2, -slot_total_h)
    .lineTo(slot_bottom_w/2, -slot_top_h)
    .lineTo(slot_top_w/2, -slot_top_h)
    .lineTo(slot_top_w/2, 0)
    .close()
)

# 3. Cut slots running along Y axis (spaced along X)
# Calculate X positions
x_positions = [
    (i - (num_slots_x - 1) / 2) * grid_pitch_x 
    for i in range(num_slots_x)
]

# We extrude the profile along Y to create the cutter
# The base is centered at Z=0, so top surface is Z=plate_height/2
# We need to move the profile to the top surface
slot_cutter_y = (
    t_profile
    .workplane(offset=plate_depth/2) # Move to the front edge
    .extrude(-plate_depth)           # Extrude backwards through the plate
)

# Move the cutter up to the top surface of the base plate
slot_cutter_y = slot_cutter_y.translate((0, 0, plate_height/2))

# Perform cuts for X-spaced slots
result = base
for x_pos in x_positions:
    cutter_instance = slot_cutter_y.translate((x_pos, 0, 0))
    result = result.cut(cutter_instance)

# 4. Cut slots running along X axis (spaced along Y)
# We need a new profile oriented on YZ plane
t_profile_x = (
    cq.Workplane("YZ")
    .moveTo(-slot_top_w/2, 0)
    .lineTo(-slot_top_w/2, -slot_top_h)
    .lineTo(-slot_bottom_w/2, -slot_top_h)
    .lineTo(-slot_bottom_w/2, -slot_total_h)
    .lineTo(slot_bottom_w/2, -slot_total_h)
    .lineTo(slot_bottom_w/2, -slot_top_h)
    .lineTo(slot_top_w/2, -slot_top_h)
    .lineTo(slot_top_w/2, 0)
    .close()
)

y_positions = [
    (i - (num_slots_y - 1) / 2) * grid_pitch_y 
    for i in range(num_slots_y)
]

slot_cutter_x = (
    t_profile_x
    .workplane(offset=plate_width/2)
    .extrude(-plate_width)
)

slot_cutter_x = slot_cutter_x.translate((0, 0, plate_height/2))

for y_pos in y_positions:
    cutter_instance = slot_cutter_x.translate((0, y_pos, 0))
    result = result.cut(cutter_instance)
