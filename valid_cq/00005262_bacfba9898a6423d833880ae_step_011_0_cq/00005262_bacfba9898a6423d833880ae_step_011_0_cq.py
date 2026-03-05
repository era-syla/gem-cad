import cadquery as cq

# --- Parametric Variables ---
# Main Plate Dimensions
plate_width = 120.0
plate_length = 80.0
plate_thickness = 2.0
corner_radius = 5.0

# Hole Grid Parameters
small_hole_diameter = 3.2  # M3 clearance
large_hole_diameter = 4.2  # M4 clearance (or similar mounting points)

# Slot Parameters
slot_length = 15.0
slot_width = 3.2

# Underside Feature Parameters
bracket_width = 10.0
bracket_depth = 12.0
bracket_hole_dia = 3.2
standoff_dia = 6.0
standoff_height = 5.0

# --- Geometry Construction ---

# 1. Base Plate
# Create the main rectangular plate with rounded corners
plate = (
    cq.Workplane("XY")
    .rect(plate_width, plate_length)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Pattern Generation
# Analyzing the image, the hole pattern is somewhat irregular but follows a grid.
# Instead of exact pixel-perfect coordinates (impossible to know from one image),
# we will create a dense grid and then selectively remove/modify or build 
# specific patterns that mimic the visual density and arrangement.

# Let's define lists of coordinates based on visual estimation of the grid
# The grid appears to be roughly 10mm spacing.

# 2a. The dense grid of small holes in the middle
# We'll generate a grid and then cut.
grid_w = 9  # Number of columns
grid_h = 6  # Number of rows
spacing_x = 10.0
spacing_y = 10.0

small_holes = []
for i in range(grid_w):
    for j in range(grid_h):
        # Center the grid
        x = (i * spacing_x) - ((grid_w - 1) * spacing_x / 2)
        y = (j * spacing_y) - ((grid_h - 1) * spacing_y / 2)
        
        # Skip center area where larger features or gaps might be (visual approximation)
        if -15 < x < 15 and -15 < y < 15:
            continue 
        
        small_holes.append((x, y))

# Cut the small grid holes
result = plate.faces(">Z").workplane().pushPoints(small_holes).hole(small_hole_diameter)

# 2b. Larger holes
# These appear near the center and edges
large_hole_locs = [
    (0, 0),       # Center
    (30, 0), (-30, 0),
    (0, 20), (0, -20),
    (45, 25), (-45, 25),
    (45, -25), (-45, -25),
    (20, 20), (-20, 20),
    (20, -20), (-20, -20)
]
result = result.faces(">Z").workplane().pushPoints(large_hole_locs).hole(large_hole_diameter)

# 2c. Slots
# The image shows slots near the short edges (left and right in the image orientation)
# Let's place them symmetrically.
slot_centers = [
    (40, 30), (-40, 30), # Top outer slots
    (40, -30), (-40, -30) # Bottom outer slots
]

# Create slots by making a sketch or using slot2D
slot_locations = result.faces(">Z").workplane()
for x, y in slot_centers:
    # Orient slots along X axis
    result = result.faces(">Z").workplane(centerOption="CenterOfMass").center(x, y).slot2D(slot_length, slot_width).cutThruAll()


# 3. Underside Features (Brackets/Standoffs)
# The image shows features protruding from the bottom.

# 3a. Standoffs (cylinders)
standoff_locs = [
    (25, 0), (-25, 0)
]

for x, y in standoff_locs:
    # Create cylinder
    standoff = (
        cq.Workplane("XY")
        .workplane(offset=0) # Bottom plane (Z=0)
        .center(x, y)
        .circle(standoff_dia/2)
        .extrude(-standoff_height) # Extrude downwards
    )
    # Add hole to standoff
    standoff = standoff.faces("<Z").workplane().hole(small_hole_diameter)
    result = result.union(standoff)

# 3b. Mounting Bracket (The U-shaped thing visible on the bottom edge)
# It's centered on one of the long edges (Y axis in our coordinates)
bracket_loc_y = -plate_length/2 + 5 # Slightly inset

# Create a U-bracket shape
bracket_sketch = (
    cq.Workplane("XZ") # Draw on side plane
    .workplane(offset=-plate_length/2 + bracket_width/2) # Position at the edge
    .center(0, -standoff_height/2) # Center vertically relative to standoff depth
    .rect(bracket_width, bracket_depth + 2) # Basic block
    .extrude(bracket_width) # Extrude along Y
)

# Refine bracket (add hole sideways)
bracket = (
    cq.Workplane("YZ")
    .workplane(offset=0) # Center X
    .center(-plate_length/2 + 5, -standoff_height/2 - 2)
    .circle(bracket_hole_dia/2)
    .extrude(20, both=True) # Cut hole through bracket area
)

# Since constructing the specific bracket geometry from just this angle is ambiguous,
# we will construct a simplified representation of the visible underside mounting lug.
# It looks like two tabs with a hole.

tab_dist = 6.0
tab_thick = 3.0
tab_height = 8.0
tab_width = 10.0

# Left Tab
tab1 = (
    cq.Workplane("XY")
    .workplane(offset=0) # Bottom of plate
    .center(0, -plate_length/2 + 5)
    .center(-tab_dist/2, 0)
    .rect(tab_thick, tab_width)
    .extrude(-tab_height)
)
# Right Tab
tab2 = (
    cq.Workplane("XY")
    .workplane(offset=0) # Bottom of plate
    .center(0, -plate_length/2 + 5)
    .center(tab_dist/2, 0)
    .rect(tab_thick, tab_width)
    .extrude(-tab_height)
)

# Cross hole through tabs
tabs = tab1.union(tab2)
tabs_hole = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .center(-plate_length/2 + 5, -tab_height/2)
    .circle(small_hole_diameter/2)
    .extrude(20, both=True)
)

tabs_final = tabs.cut(tabs_hole)
result = result.union(tabs_final)


# --- Final Export/Display ---
# result is the final object