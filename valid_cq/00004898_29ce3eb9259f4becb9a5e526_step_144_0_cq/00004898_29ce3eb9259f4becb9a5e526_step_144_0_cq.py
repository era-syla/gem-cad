import cadquery as cq

# Define parametric dimensions
thickness = 3.0    # Thickness of the plate
width = 80.0       # Horizontal width of the plate
height = 80.0      # Vertical height of the plate
chamfer_size = 15.0 # Size of the small chamfers on the 90-degree corners (estimated)
cut_corner_size = 20.0 # The offset from the corners where the large angled cut begins

hole_diameter = 6.0 # Diameter of the mounting holes
margin = 15.0       # Distance from edges to hole centers

# Create the base shape using a Workplane and a sketch
# The shape is essentially a square with one large corner cut off
# Points: (0,0) -> (width, 0) -> (width, height-cut) -> (width-cut, height) -> (0, height) -> (0,0)
# Looking at the image, it looks like a standard 5-hole joining plate (like for 2020 extrusion).
# Let's refine the shape logic. It looks like an "L" plate that has been filled in to form a triangle,
# but with the hypotenuse tip cut off.

# Let's model it as a polygon for precise control.
# Coordinates assuming bottom-left is near (0,0):
# The image shows a plate with 5 holes.
# 3 holes vertical on the left side.
# 2 additional holes extending to the right on the top side.
# This suggests a 90-degree bracket.

# Revised Dimensions based on standard extrusion plates (e.g., 2020 or 3030 series):
plate_width = 80.0
plate_height = 80.0
plate_thickness = 4.0

# The shape is an irregular pentagon.
# Point 1: Bottom Left (0, 0)
# Point 2: Top Left (0, plate_height)
# Point 3: Top Right (plate_width, plate_height)
# Point 4: Right edge, slightly down (plate_width, plate_height - some_offset)
# Point 5: Bottom edge, slightly right (some_offset, 0) - Actually, looking closer,
# the large diagonal cut connects the right side to the bottom side.

# Let's try a subtraction method: Start with a square, cut the large diagonal.
p_width = 100.0  # Estimated large side
p_height = 100.0 # Estimated large side
tip_width = 20.0 # The flat part at the ends of the triangle
hypotenuse_cut_offset = 20.0 # Where the diagonal cut starts relative to the full square corner

# Let's build the points explicitly for the outline shown in the image.
# It's an L-shaped bracket gusset.
# Orientation in image: Vertical edge on left, Horizontal edge on top (rotated).
# Let's model it flat on XY plane first.

# Points counter-clockwise starting from bottom-left (which corresponds to bottom-left in image)
p0 = (0, 0)
p1 = (plate_width, 0)  # Top edge in standard orientation, but let's stick to image visual. 
# Actually, the image shows:
# Long vertical edge on the left.
# Long horizontal edge on the top.
# Short vertical edge on the right.
# Short horizontal edge on the bottom.
# A diagonal connecting the short edges.

# Let's set dimensions relative to a standard 20mm grid spacing common in these plates.
grid_spacing = 20.0
num_holes_vertical = 3
num_holes_horizontal = 3 # Including the corner one shared

# Calculate overall size
# 3 holes -> spans roughly 3 * 20 = 60mm between outer centers + margins.
# Let's assume 20mm margin/spacing grid.
# Top-Left hole is at (10, 10) from top-left corner.
# Vertical holes at y = -10, -30, -50.
# Horizontal holes at x = 10, 30, 50.

# Overall dimensions estimate:
total_w = 60.0 # 3 spaces of 20mm
total_h = 60.0 

# Let's adjust to the visual proportion. It looks like a "90 degree Triangle Bracket".
# Usually roughly 60mm x 60mm for 2020 extrusion.
side_length = 60.0
tip_flat_length = 15.0 # The small flat edges at the ends of the diagonal

# Define points for the outline
# Origin at top-left of the image (sharp corner)
pts = [
    (0, 0),                       # Top-Left corner
    (side_length, 0),             # Top-Right corner of the bounding box
    (side_length, -tip_flat_length), # Top-Right vertical drop
    (tip_flat_length, -side_length), # Bottom-Left horizontal start of diagonal
    (0, -side_length)             # Bottom-Left corner
]
# Wait, the image shows the diagonal connecting the bottom-right.
# Let's re-orient to match the image:
# Long straight edge on Left.
# Long straight edge on Top.
# The diagonal cuts the Bottom-Right.

# Points:
# 1. Top-Left (0, 60)
# 2. Top-Right (60, 60)
# 3. Bottom-Right, up a bit (60, 15)  -> This creates the short vertical edge on the right
# 4. Bottom-Left, right a bit (15, 0) -> This creates the short horizontal edge on the bottom
# 5. Bottom-Left (0,0) is WRONG, the diagonal connects (60, 15) to (15, 0).
# The main corner is at (0, 60).

side = 60.0
tip = 15.0
thick = 4.0
h_diam = 5.5 # Clearance for M5

# Create the plate sketch
result = (
    cq.Workplane("XY")
    .polyline([
        (0, side),      # Top Left
        (side, side),   # Top Right
        (side, side - tip), # Drop down on right side
        (tip, 0),       # Diagonal to bottom edge
        (0, 0),         # Bottom Left corner
        (0, side)       # Close loop
    ])
    .close()
    .extrude(thick)
)

# Define Hole positions
# Based on 20mm spacing typical for these brackets
# Origin of our shape is (0,0) at Bottom-Left, (0, side) is Top-Left.
# We need to place holes relative to the Top-Left corner (0, side) and the axes.

# Vertical holes (along x=10 relative to left edge)
# Positions from Top-Left (0, 60):
# 1. (10, 50)  -> 10mm right, 10mm down
# 2. (10, 30)  -> 10mm right, 30mm down
# 3. (10, 10)  -> 10mm right, 50mm down 
# wait, (0,0) is bottom left. 
# y=50 is 10mm from top.
# y=30 is 30mm from top.
# y=10 is 50mm from top.

holes_vertical = [
    (10, side - 10),
    (10, side - 30),
    (10, side - 50)
]

# Horizontal holes (along top edge y=50 relative to bottom)
# We already have the corner hole at (10, side-10).
# We need holes to the right.
# Positions from Top-Left:
# 1. (30, 50) -> 30mm right, 10mm down
# 2. (50, 50) -> 50mm right, 10mm down

holes_horizontal = [
    (30, side - 10),
    (50, side - 10)
]

all_holes = holes_vertical + holes_horizontal

# Cut the holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(all_holes)
    .hole(h_diam)
)

# Optional: Rotate to match image orientation roughly
# Image has long vertical edge on left, long angled edge on right.
# Our model has long vertical on left, long horizontal on top.
# It matches the image if we look at it isometrically.