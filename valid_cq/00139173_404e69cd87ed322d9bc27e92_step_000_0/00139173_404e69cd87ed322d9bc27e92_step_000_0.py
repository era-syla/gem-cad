import cadquery as cq

# --- Parameters ---
length = 240.0        # Total length of the panel
height = 60.0         # Total height of the panel
thickness = 4.0       # Thickness of the material

num_sections = 3      # Number of vertical sections (bays)
num_slots = 4         # Number of horizontal slots per section

frame_width = 5.0     # Width of the outer border
divider_width = 5.0   # Width of the vertical dividers between sections
bar_height = 3.0      # Height of the horizontal bars (slats)

# --- derived dimensions ---
# Calculate the width of each open bay
total_h_gaps = (num_sections - 1) * divider_width + 2 * frame_width
bay_width = (length - total_h_gaps) / num_sections

# Calculate the height of each slot
total_v_gaps = (num_slots - 1) * bar_height + 2 * frame_width
slot_height = (height - total_v_gaps) / num_slots

# --- Modeling ---

# 1. Create the base solid block
base = cq.Workplane("XY").box(length, height, thickness)

# 2. Generate center points for the cutouts
cutout_points = []

# Calculate the starting center position (bottom-left slot)
start_x = -length/2 + frame_width + bay_width/2
start_y = -height/2 + frame_width + slot_height/2

for i in range(num_sections):
    # X position for the current section
    x_pos = start_x + i * (bay_width + divider_width)
    
    for j in range(num_slots):
        # Y position for the current slot
        y_pos = start_y + j * (slot_height + bar_height)
        cutout_points.append((x_pos, y_pos))

# 3. Cut the slots into the base
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(cutout_points)
    .rect(bay_width, slot_height)
    .cutThruAll()
)