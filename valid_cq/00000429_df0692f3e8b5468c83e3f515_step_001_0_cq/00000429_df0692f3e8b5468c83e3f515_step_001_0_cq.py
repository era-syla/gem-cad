import cadquery as cq

# --- Parameters ---
wall_length = 3000.0   # Total length of the wall
wall_height = 2400.0   # Total height of the wall
stud_width = 45.0      # Width of the timber (e.g., 2x4 narrow side)
stud_depth = 90.0      # Depth of the timber (e.g., 2x4 wide side)

# Opening (Doorway/Window) parameters
opening_width = 1000.0 
opening_height = 2100.0 # Height of the header from floor
opening_offset = 1200.0 # Distance from left edge to start of opening

# Stud spacing
stud_spacing = 400.0   # Center-to-center spacing

# --- Helper Functions ---

def make_stud(length, width, depth):
    return cq.Workplane("XY").box(width, depth, length)

def make_plate(length, width, depth):
    return cq.Workplane("XY").box(length, depth, width)

# --- Construction ---

# 1. Top Plate
top_plate = make_plate(wall_length, stud_width, stud_depth)
top_plate = top_plate.translate((wall_length/2, 0, wall_height - stud_width/2))

# 2. Bottom Plate (needs a gap for the opening)
# Left segment
bottom_plate_left_len = opening_offset
bottom_plate_left = make_plate(bottom_plate_left_len, stud_width, stud_depth)
bottom_plate_left = bottom_plate_left.translate((bottom_plate_left_len/2, 0, stud_width/2))

# Right segment
bottom_plate_right_len = wall_length - (opening_offset + opening_width)
bottom_plate_right = make_plate(bottom_plate_right_len, stud_width, stud_depth)
bottom_plate_right = bottom_plate_right.translate((wall_length - bottom_plate_right_len/2, 0, stud_width/2))

# 3. Vertical Studs
studs = []

# Calculate stud positions
current_x = 0
stud_positions = []
while current_x <= wall_length:
    # Check if this stud falls within the opening
    in_opening = (current_x > opening_offset + stud_width) and (current_x < opening_offset + opening_width - stud_width)
    
    # Check if this is a king stud (borders of the opening)
    is_left_king = abs(current_x - opening_offset) < stud_width
    is_right_king = abs(current_x - (opening_offset + opening_width)) < stud_width
    
    if not in_opening:
        stud_positions.append(current_x)
    
    # Advance to next stud, aligning to the grid or special positions
    next_grid = (int(current_x / stud_spacing) + 1) * stud_spacing
    
    # If the next grid point is past the end, break
    if next_grid > wall_length and current_x != wall_length:
        if wall_length not in stud_positions:
             stud_positions.append(wall_length)
        break
    
    current_x = next_grid

# Ensure start and end studs are present
if 0 not in stud_positions: stud_positions.insert(0, 0)
if wall_length not in stud_positions: stud_positions.append(wall_length)

# Ensure framing around opening (King Studs)
if opening_offset not in stud_positions: 
    stud_positions.append(opening_offset)
if (opening_offset + opening_width) not in stud_positions: 
    stud_positions.append(opening_offset + opening_width)

stud_positions.sort()

# Generate the stud geometry
for pos in stud_positions:
    x_center = pos
    
    # Adjust center for end studs to be flush
    if pos == 0: x_center = stud_width / 2
    elif pos == wall_length: x_center = wall_length - stud_width / 2
    # Adjust center for opening studs to be flush with opening edge
    elif abs(pos - opening_offset) < 1.0: x_center = opening_offset - stud_width / 2
    elif abs(pos - (opening_offset + opening_width)) < 1.0: x_center = (opening_offset + opening_width) + stud_width / 2
    
    # Create the full height stud
    s = make_stud(wall_height - 2*stud_width, stud_width, stud_depth) # Subtract top/bottom plates
    s = s.translate((x_center, 0, wall_height/2))
    studs.append(s)

# 4. Opening Header / Sill
# Based on the image, there is a horizontal piece connecting the opening studs at the bottom
# This acts like a threshold or a continuous plate connection in some framing styles, 
# or a sill for a large window/door. In the image, it looks like a bottom plate connector.
threshold = make_plate(opening_width, stud_width, stud_depth)
threshold = threshold.translate((opening_offset + opening_width/2, 0, stud_width/2))

# Combine all parts
result = top_plate.union(bottom_plate_left).union(bottom_plate_right).union(threshold)

for s in studs:
    result = result.union(s)

# Center the whole assembly
result = result.translate((-wall_length/2, 0, 0))