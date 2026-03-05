import cadquery as cq

# --- Dimensions ---
plate_length = 200.0
plate_width = 100.0
plate_thickness = 2.0

bump_diameter = 5.0
bump_height = 1.0

# --- Pattern Configuration ---
num_rows = 5
cols_wide = 11   # Number of bumps in odd rows (1, 3, 5)
cols_narrow = 10 # Number of bumps in even rows (2, 4)
pitch_x = 16.0   # Horizontal spacing
pitch_y = 14.0   # Vertical spacing

# --- Geometry Generation ---

# 1. Generate coordinates for the staggered grid
bump_locations = []

# Calculate total height of the pattern to center it vertically
total_pattern_height = (num_rows - 1) * pitch_y
start_y = -total_pattern_height / 2.0

for row in range(num_rows):
    current_y = start_y + row * pitch_y
    
    # Determine row type for staggering
    if row % 2 == 0:
        # Wide row (aligned with edges)
        current_cols = cols_wide
    else:
        # Narrow row (indented)
        current_cols = cols_narrow
        
    # Calculate total width of this row to center it horizontally
    row_width = (current_cols - 1) * pitch_x
    start_x = -row_width / 2.0
    
    for col in range(current_cols):
        current_x = start_x + col * pitch_x
        bump_locations.append((current_x, current_y))

# 2. Create the Base Plate
# Create a box centered on the XY plane
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 3. Add the Patterned Bumps
# Select the top face, push the generated points, draw circles, and extrude
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(bump_locations)
    .circle(bump_diameter / 2.0)
    .extrude(bump_height)
)