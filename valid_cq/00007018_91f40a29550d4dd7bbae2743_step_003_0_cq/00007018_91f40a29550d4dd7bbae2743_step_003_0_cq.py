import cadquery as cq

# --- Parametric Dimensions ---
# Overall plate dimensions
width = 100.0   # X dimension
height = 80.0   # Y dimension
thickness = 3.0 # Z dimension
corner_radius = 5.0

# Grid parameters
num_rows = 7    # Total rows of holes
num_cols = 7    # Total columns of holes

# Hole specifications
# Large holes (countersunk/counterbored appearance)
large_hole_diam = 6.0
large_csk_diam = 8.0
large_csk_angle = 82.0

# Small holes
small_hole_diam = 2.5

# --- Geometry Construction ---

# 1. Create the base plate
# We center it to make grid calculations easier
plate = (
    cq.Workplane("XY")
    .box(width, height, thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Define the Grid and Hole Locations
# The pattern is an alternating grid.
# Looking at the image, it's a 7x7 grid (roughly). 
# Rows alternate between Large holes and Small holes, but offset.
# Actually, it looks like a checkerboard pattern.
# Let's verify the pattern visually:
# Row 1 (top): Small, Large, Small, Large, Small, Large, Small
# Row 2: Large, Small, Large, Small, Large, Small, Large
# ... and so on.

# Calculate spacing
# We want margins on the edges. Let's assume uniform spacing.
margin_x = 10.0
margin_y = 10.0

spacing_x = (width - 2 * margin_x) / (num_cols - 1)
spacing_y = (height - 2 * margin_y) / (num_rows - 1)

large_hole_locs = []
small_hole_locs = []

# Generate coordinates based on a centered logic
start_x = -width / 2 + margin_x
start_y = -height / 2 + margin_y

for row in range(num_rows):
    for col in range(num_cols):
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y
        
        # Determine hole type based on checkerboard logic (row index + col index)
        # Looking at the reference, the corners are large holes in some variations or small in others.
        # Let's match the image: Bottom-left corner is a Large hole.
        # Let's assume (0,0) is bottom-left. 
        if (row + col) % 2 == 0:
            large_hole_locs.append((x, y))
        else:
            small_hole_locs.append((x, y))

# 3. Apply the Holes

# Add Large Holes (Countersunk)
result = (
    plate
    .faces(">Z")
    .workplane()
    .pushPoints(large_hole_locs)
    .cskHole(large_hole_diam, large_csk_diam, large_csk_angle)
)

# Add Small Holes (Simple through holes)
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(small_hole_locs)
    .hole(small_hole_diam)
)

# Return result for display
if 'show_object' in locals():
    show_object(result)