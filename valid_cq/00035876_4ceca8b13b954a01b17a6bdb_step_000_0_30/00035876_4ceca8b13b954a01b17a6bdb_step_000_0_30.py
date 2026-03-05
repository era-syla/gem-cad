import cadquery as cq

# --- Model Parameters ---
length = 90.0          # Total length of the bench
width = 36.0           # Total width of the bench
thickness = 4.0        # Thickness of the top platform
leg_height = 25.0      # Height of the legs
leg_profile = 4.0      # Square size of the leg cross-section

# Grid Layout Parameters
frame_margin = 2.5     # Width of the outer frame border
mid_rib_width = 5.0    # Width of the central transverse divider
num_slots = 6          # Number of slots along the width
rib_gap = 2.0          # Thickness of ribs between slots

# --- Calculations ---
# Calculate the dimensions of individual slot holes
# Available length for slots (divided by 2 for left/right sections)
slot_length = (length - (2 * frame_margin) - mid_rib_width) / 2.0

# Available width for slots
available_width = width - (2 * frame_margin)
# Calculate slot width: Total space minus total gaps, divided by number of slots
slot_width = (available_width - (num_slots - 1) * rib_gap) / num_slots

# Generate center points for the slot cutouts
slot_points = []
# X coordinates for the two columns (left and right of center)
x_offset = (mid_rib_width / 2.0) + (slot_length / 2.0)
x_coords = [-x_offset, x_offset]

# Y coordinates for the rows
# Starting Y center: bottom edge + margin + half slot width
y_start = -(width / 2.0) + frame_margin + (slot_width / 2.0)
y_pitch = slot_width + rib_gap # Distance between slot centers

for x in x_coords:
    for i in range(num_slots):
        y = y_start + (i * y_pitch)
        slot_points.append((x, y))

# Determine Leg Positions (inset from corners)
leg_inset_x = 15.0
# Inset Y to align roughly inside the outer frame
leg_inset_y = frame_margin + (leg_profile / 2.0) 
leg_x_loc = (length / 2.0) - leg_inset_x
leg_y_loc = (width / 2.0) - leg_inset_y

leg_points = [
    (leg_x_loc, leg_y_loc),
    (leg_x_loc, -leg_y_loc),
    (-leg_x_loc, leg_y_loc),
    (-leg_x_loc, -leg_y_loc)
]

# --- Geometry Construction ---

# 1. Create the solid base block
base = cq.Workplane("XY").box(length, width, thickness)

# 2. Cut the array of slots through the base
grate = (
    base.faces(">Z")
    .workplane()
    .pushPoints(slot_points)
    .rect(slot_length, slot_width)
    .cutBlind(-thickness)
)

# 3. Extrude legs from the bottom surface
result = (
    grate.faces("<Z")
    .workplane()
    .pushPoints(leg_points)
    .rect(leg_profile, leg_profile)
    .extrude(leg_height)
)