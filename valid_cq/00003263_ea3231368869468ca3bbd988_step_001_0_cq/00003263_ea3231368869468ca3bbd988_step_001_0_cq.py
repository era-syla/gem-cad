import cadquery as cq

# --- Parameters ---
# Main plate dimensions
plate_width = 150.0
plate_length = 200.0
plate_thickness = 3.0

# Mounting holes (corner holes + mid-edge holes)
mounting_hole_dia = 4.0
mounting_inset = 6.0  # Distance from edge

# Keypad holes (3x4 grid roughly)
# Looking at image:
# Left side has a cluster of circular holes.
# There are 3 columns, roughly 4 rows, but the top-left one is missing or shifted?
# Actually, it looks like a standard numpad layout (1-9, *, 0, #) plus maybe some extra buttons?
# Let's approximate a grid of circular holes on the left side.
key_hole_dia = 12.0
key_grid_x_spacing = 20.0
key_grid_y_spacing = 20.0
# Position of the key grid center relative to plate center
key_grid_center_x = -plate_width/4.0 
key_grid_center_y = 20.0

# There is a larger, slightly offset hole near the top of the keypad area
indicator_hole_dia = 10.0
indicator_hole_pos = (-plate_width/4.0 + 25, 60.0)

# Display Cutout (rectangular)
display_width = 80.0
display_height = 50.0
# Position on the right side
display_center_x = plate_width/4.0
display_center_y = -30.0

# Ball/Knob Feature
# Attached to the "top" edge (relative to the orientation). 
# In the image, it's protruding from the back edge.
ball_dia = 50.0
# It seems to be mounted on a cylindrical stalk or directly attached.
ball_z_offset = plate_thickness # Sits on top or flush? Let's assume flush with top face or slightly intersected.
ball_y_pos = plate_length/2.0  # At the very edge
ball_x_pos = -plate_width/4.0  # Aligned somewhat with the keypad column

# --- Modeling ---

# 1. Create the base plate
plate = cq.Workplane("XY").box(plate_width, plate_length, plate_thickness)

# 2. Create Mounting Holes
# We need holes at corners and mid-points of long edges
# Locations relative to center (0,0)
xs = [plate_width/2.0 - mounting_inset, -plate_width/2.0 + mounting_inset]
ys = [plate_length/2.0 - mounting_inset, -plate_length/2.0 + mounting_inset, 0]

mounting_pts = []
for x in xs:
    for y in ys:
        mounting_pts.append((x, y))

# Add mid-points for the short edges as well? Image shows 3 along side, maybe 2 along top/bottom?
# Let's look closely. It looks like 3 holes along the long edges, and 2 along the short edges (corners only).
# The loop above creates a 2x3 grid which matches: corners + mid-sides.
plate = plate.faces(">Z").workplane().pushPoints(mounting_pts).hole(mounting_hole_dia)

# 3. Create Keypad Holes
# Let's define a specific set of points for the keys to match the image better.
# It looks like 3 columns.
# Left column: 3 holes
# Middle column: 4 holes
# Right column: 3 holes
# Let's approximate positions relative to the grid center defined earlier.

key_pts = []
# Columns
cols = [-key_grid_x_spacing, 0, key_grid_x_spacing]
# Rows (from bottom to top)
rows = [-1.5*key_grid_y_spacing, -0.5*key_grid_y_spacing, 0.5*key_grid_y_spacing, 1.5*key_grid_y_spacing]

# Generating a pattern similar to the image
# It looks like a 3x3 grid with an extra one at the bottom middle (0 key)
# plus maybe one at top right?
# Let's simpler: 4 rows, 3 cols, remove specific ones to match 'look'.
# Image:
# Col 1 (left): 3 holes (bottom 3 rows)
# Col 2 (mid): 4 holes (all rows)
# Col 3 (right): 3 holes (bottom 3 rows)
# Plus the indicator hole separate.

for i, col_x in enumerate(cols):
    for j, row_y in enumerate(rows):
        # Center the grid logic
        abs_x = key_grid_center_x + col_x
        abs_y = key_grid_center_y + row_y
        
        # Skip top row for left and right columns to match visual density
        if j == 3 and (i == 0 or i == 2):
            continue
            
        key_pts.append((abs_x, abs_y))

plate = plate.faces(">Z").workplane().pushPoints(key_pts).hole(key_hole_dia)

# 4. Indicator Hole (top right of keypad cluster)
plate = plate.faces(">Z").workplane().pushPoints([indicator_hole_pos]).hole(indicator_hole_dia)

# 5. Rectangular Display Cutout
plate = (plate.faces(">Z").workplane()
         .center(display_center_x, display_center_y)
         .rect(display_width, display_height)
         .cutBlind(-plate_thickness))

# 6. The Ball/Dome feature
# In the image, this looks like a sphere intersected with the back edge of the plate.
# We will create a sphere and union it.
sphere = cq.Workplane("XY").sphere(ball_dia/2.0)

# Position the sphere. 
# It is located at the back edge (Y max), offset to the left side (negative X).
# Z position: Center of sphere needs to be handled carefully. 
# Image shows it protruding upwards.
sphere = sphere.translate((ball_x_pos, ball_y_pos, 0))

# Combine plate and sphere
result = plate.union(sphere)

# Export or Render
if 'show_object' in globals():
    show_object(result)