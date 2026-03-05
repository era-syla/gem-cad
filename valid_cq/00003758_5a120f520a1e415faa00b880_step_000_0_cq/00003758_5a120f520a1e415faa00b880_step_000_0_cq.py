import cadquery as cq

# --- Parametric Dimensions ---
# Overall plate dimensions
plate_width = 240.0
plate_height = 160.0
plate_thickness = 2.0

# Hole specifications
hole_size = 4.0  # Square hole side length

# --- Hole Coordinates ---
# Based on visual approximation of the grid pattern.
# The coordinates are relative to the center of the plate (0,0).
# Let's define the positions carefully based on the image's groupings.

# Right column (6 holes)
right_col_x = plate_width/2 - 20 
right_col_y_start = 60
right_col_spacing = 20
right_holes = [(right_col_x, right_col_y_start - i * right_col_spacing) for i in range(6)]

# Middle-ish column (6 holes) - looks slightly left of center
mid_col_x = -plate_width/2 + 80
mid_col_y_start = 30
mid_col_spacing = 20
mid_holes = [(mid_col_x, mid_col_y_start - i * mid_col_spacing) for i in range(6)]

# Left top horizontal pair
left_top_y = plate_height/2 - 20
left_top_holes = [(-plate_width/2 + 20, left_top_y), (-plate_width/2 + 35, left_top_y - 5)] 
# Actually, looking closer, let's refine the pattern.
# It seems to be a VEX Robotics style plate or similar structural component.
# Let's map coordinates assuming a roughly 20mm grid or similar standard spacing.

# Let's restart coordinate mapping relative to a center origin (0,0)
# Plate is approx 12x8 "units" wide/high based on typical hole spacing.
# Let's stick to absolute mm positions for robustness.

holes = []

# Vertical column on the far right
x_right = 90
y_start_right = 60
for i in range(6):
    holes.append((x_right, y_start_right - i * 20))

# Vertical column near left-center
x_mid = -30
y_start_mid = 30
for i in range(6):
    holes.append((x_mid, y_start_mid - i * 20))

# Scattered holes on the left side
holes.append((-100, 40))  # Top left-ish
holes.append((-100, 20))  # Below that
holes.append((-100, -20)) # Further down

holes.append((-80, 45))   # Top row, slightly right of edge
holes.append((-95, 45))   # Top row, near edge

holes.append((-80, -30))  # Lower section
holes.append((-90, -50))  # Lower section
holes.append((-30, -70))  # Bottom edge, aligned with mid column
holes.append((-60, -80))  # Bottom edge area? No, looks like (-30, -70) is correct.

# Re-evaluating based on grid alignment. 
# It looks like standard VEX EDR 5x25 or similar plate, but trimmed.
# Let's just place holes explicitly to match visual features.

# Group 1: The vertical stack on the right
# 6 holes
grp1_x = 80
grp1_y = [65, 50, 35, 20, 5, -10] 
# Based on image, these are near the top right corner.

# Group 2: The vertical stack in the middle-left
# 6 holes
grp2_x = -20
grp2_y = [40, 25, 10, -5, -20, -35]

# Group 3: The left edge holes
# 2 holes
grp3_x = -100
grp3_y = [15, -15]

# Group 4: Top Left Corner horizontal-ish pair
grp4 = [(-90, 55), (-75, 50)]

# Group 5: Scattered single holes
single_holes = [
    (-75, -25),  # Middle left low
    (-90, -45),  # Bottom left low
    (-30, -75),  # Bottom edge center
    (90, -60),   # Bottom right single hole
    (110, -15),  # Far right single hole
]

# Let's consolidate into a cleaner list of (x,y) tuples
pts = []

# Right Column (6 holes)
for i in range(6):
    pts.append((80, 60 - i*20))

# Middle Column (6 holes)
for i in range(6):
    pts.append((-20, 40 - i*20))

# Left Column (2 holes)
pts.append((-100, 10))
pts.append((-100, -20))

# Top Left edge
pts.append((-90, 55))  # Topmost left
pts.append((-75, 50))  # Next to it

# Random scattered
pts.append((-75, -30)) 
pts.append((-90, -55))
pts.append((-30, -75)) # Bottom center-ish
pts.append((90, -50))  # Bottom right area
pts.append((110, -10)) # Mid right edge area

# --- Model Creation ---

# 1. Create the base plate
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Cut the square holes
# We use a custom workplane on the top face to sketch the squares
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(pts)
    .rect(hole_size, hole_size)
    .cutThruAll()
)

# Optional: Fillet the corners of the plate slightly for realism? 
# The image shows sharp corners, so we will leave them sharp.