import cadquery as cq

# --- Parameter Definitions ---
bench_length = 100.0      # Total length of the bench
bench_width = 40.0        # Total width of the bench
top_thickness = 5.0       # Thickness of the top platform
frame_width = 3.0         # Width of the outer frame border
mid_divider_width = 6.0   # Width of the central divider bar
leg_height = 35.0         # Height of the legs
leg_inset = 15.0          # Distance legs are inset from the short ends
num_slots = 6             # Number of slots (gaps) across the width

# --- Derived Dimensions ---
# Calculate the available width inside the frame for the slats
internal_width = bench_width - (2 * frame_width)

# Calculate slot (gap) and slat widths assuming they are equal
# Formula: num_slots * w + (num_slots - 1) * w = internal_width
# (2 * num_slots - 1) * w = internal_width
slot_width = internal_width / (2 * num_slots - 1)
slat_width = slot_width

# Calculate the length of a single slot
# (Total length - 2 * frame - middle divider) / 2
slot_length = (bench_length - (2 * frame_width) - mid_divider_width) / 2.0

# --- Geometry Construction ---

# 1. Base Platform
# Create the solid block representing the top
result = cq.Workplane("XY").box(bench_length, bench_width, top_thickness)

# 2. Cut Slots (Grill Pattern)
# We calculate the center points for all rectangular cuts
cut_centers = []

# X Coordinates: Centers of the left and right slot columns
# Left side center: - (half divider + half slot length)
# Right side center: + (half divider + half slot length)
x_centers = [
    -(mid_divider_width / 2.0 + slot_length / 2.0),
    (mid_divider_width / 2.0 + slot_length / 2.0)
]

# Y Coordinates: Distribute slots evenly
# Start Y: bottom edge + frame + half slot width
y_start = -bench_width / 2.0 + frame_width + slot_width / 2.0

for i in range(num_slots):
    y_pos = y_start + i * (slot_width + slat_width)
    for x_pos in x_centers:
        cut_centers.append((x_pos, y_pos))

# Execute the cut through the top plate
result = (result.faces(">Z")
          .workplane()
          .pushPoints(cut_centers)
          .rect(slot_length, slot_width)
          .cutThruAll())

# 3. Add Legs
# We'll use a square profile for the legs matching the frame width
leg_size = frame_width

# Centers for the 4 legs
# Inset from X ends, aligned with the Y frame centerline to be flush with sides
leg_x_loc = bench_length / 2.0 - leg_inset
leg_y_loc = bench_width / 2.0 - frame_width / 2.0

leg_locations = [
    (-leg_x_loc, -leg_y_loc), 
    (leg_x_loc, -leg_y_loc),
    (-leg_x_loc, leg_y_loc),  
    (leg_x_loc, leg_y_loc)
]

# Extrude legs from the bottom face
# Note: Extruding from the bottom face (which has normal -Z) with a positive value
# extends the geometry downwards in the -Z direction.
result = (result.faces("<Z")
          .workplane()
          .pushPoints(leg_locations)
          .rect(leg_size, leg_size)
          .extrude(leg_height))

# The variable 'result' contains the final geometry