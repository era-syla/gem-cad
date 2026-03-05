import cadquery as cq
import math

# --- Parameters ---
# Plate dimensions
plate_width = 150.0
plate_height = 80.0
plate_thickness = 5.0

# Hexagon pattern parameters
hex_radius = 10.0  # circumradius (center to vertex)
hex_wall_thickness = 3.0  # Spacing between hexagons
hex_rotation = 90.0 # Rotate hexagon so flat side is vertical or horizontal

# Derived geometry
# The distance from center to flat edge (apothem)
apothem = hex_radius * math.cos(math.radians(30))
# Horizontal spacing (center-to-center) = 1.5 * radius + spacing_component? 
# For tight packing: dx = 1.5 * R, dy = 2 * apothem.
# With wall thickness:
#   The center-to-center distance needs to account for the gap.
#   Let's define spacing based on the apothem and desired gap.
x_spacing = (3/2) * hex_radius + (hex_wall_thickness * math.cos(math.radians(30))) 
y_spacing = 2 * apothem + hex_wall_thickness

# Manually defining the grid points based on the visual pattern
# The pattern looks like a staggered grid.
# Row 0 (Center): 3 hexes
# Row 1 (Top): 3 hexes, shifted
# Row -1 (Bottom): 3 hexes, shifted
# Wait, looking closer at the image:
# Central horizontal row: 3 hexagons.
# Top offset row: 3 hexagons (one clearly on the left, one middle, one right)
# Bottom offset row: 4 hexagons? No, let's count precisely.
# Top row: 3 hexes
# Middle row: 3 hexes
# Bottom row: 3 hexes
# The pattern is somewhat irregular or cropped.
# Let's recreate the specific layout shown:
# 1. A central chain of 3.
# 2. A "top" chain of 3, shifted right relative to the center.
# 3. A "bottom" chain of 3, shifted left relative to the center.
# Actually, let's use the standard hexagonal grid logic `rpush` in CadQuery creates.
# It usually creates a rectangular array of hexes.
# The image shows a specific non-rectangular cluster.
# Let's use `pushPoints` with explicit coordinates to match the image exactly.

# Coordinates estimation (relative to center (0,0))
# Let dx be horizontal step, dy be vertical step.
# In a pointy-topped hex grid (rotated 90 deg from flat-topped):
#   X step = sqrt(3) * radius
#   Y step = 1.5 * radius
# In the image, the flat sides are top/bottom. This is "flat-topped".
#   X step = 1.5 * radius  (actually 1.5 * side_len) ?
#   Let's stick to simple trigonometry.

# Flat-topped Hexagon orientation
# Width = 2 * Radius
# Height = 2 * Apothem = sqrt(3) * Radius

dx = 1.5 * hex_radius + (hex_wall_thickness * 0.866) # Approximate spacing adjustments
dy = (math.sqrt(3) * hex_radius) + hex_wall_thickness

# Let's define the specific lattice locations relative to a center point.
# We will construct a list of (col, row) logical coordinates and convert to physical (x,y).
# For flat-topped hexes, odd columns are typically shifted vertically by half a hex height.

locations_logical = [
    # Top Row
    (-1, 1), (0, 1), (1, 1),
    # Middle Row
    (-1, 0), (0, 0), (1, 0),
    # Bottom Row
    (-1, -1), (0, -1), (1, -1),
    # The image has a specific staggered look. 
    # Let's look at the "columns". 
    # Left-most: One hex
    # Next: Two hexes
    # Middle: Three hexes
    # Next: Two hexes
    # Right-most: One hex
    # This forms a diamond/rhombus shape of 3x3 if viewed diagonally.
]

# Let's try a different approach to match the visual exactly.
# The visual shows:
# Row 1 (top): 3 items
# Row 0 (mid): 3 items
# Row -1 (bot): 3 items
# BUT, they are staggered.
# Row 0 is centered.
# Row 1 is shifted Left.
# Row -1 is shifted Right.
# (Or vice-versa depending on how you look at the stagger)

# Let's assume standard staggered hex grid logic.
# If col is even, y = row * dy
# If col is odd, y = row * dy + dy/2

points = []

# Recalculate generic spacing for a flat-topped orientation
# width_hex = 2 * hex_radius
# height_hex = math.sqrt(3) * hex_radius
horizontal_dist = 1.5 * hex_radius + hex_wall_thickness 
vertical_dist = (math.sqrt(3) * hex_radius) + hex_wall_thickness

# Let's just define offsets manually to match the picture's specific cluster
# Center
points.append((0, 0)) 
# Left of center
points.append((-horizontal_dist, 0))
# Right of center
points.append((horizontal_dist, 0))

# Top Row (shifted left by half horizontal spacing? No, standard hex grid shift)
# In flat-topped, columns shift vertically. In pointy-topped, rows shift horizontally.
# The image shows flat-topped hexagons.
# Flat-topped hexagons tile such that:
#   Neighbors are at angles 0, 60, 120, 180, 240, 300.
#   0 deg: (dist_x, 0) -> Right neighbor
#   60 deg: (dist_x * cos(60), dist_y * sin(60)) -> Top-Right
#   120 deg: (-dist_x * cos(60), dist_y * sin(60)) -> Top-Left
# Where dist is center-to-center distance.
c2c = (math.sqrt(3) * hex_radius) + hex_wall_thickness # Center-to-center distance roughly
# Let's calculate precise vectors.
# Vector length D = 2 * apothem + wall_thickness.
# Actually, for flat topped, the "width" flat-to-flat is sqrt(3)*R.
# So distance between flat sides is sqrt(3)*R + wall.
D = (math.sqrt(3) * hex_radius) + hex_wall_thickness

# Basis vectors for flat-topped hex grid
v1 = (D * math.cos(math.radians(30)), D * math.sin(math.radians(30))) # 30 deg
v2 = (0, D) # 90 deg? No.
# Standard basis:
# a = (sqrt(3)/2 * D, 0.5 * D)
# b = (0, D) -> No
# Let's use simple coordinate offsets based on visual inspection of neighbors.
# dx = Horizontal distance between adjacent columns
dx = (1.5 * hex_radius) + (hex_wall_thickness / math.cos(math.radians(30))/2) # Approximate
# dy = Vertical distance between rows in same column
dy = (math.sqrt(3) * hex_radius) + hex_wall_thickness
# shift_y = Vertical shift for odd columns
shift_y = dy / 2.0

# Refined Spacing Logic based on geometry:
# Flat-topped Hexagon.
# Distance center to side = R * sqrt(3)/2
# Gap = W
# Center-to-Center Vertical = 2 * (R * sqrt(3)/2) + W = R*sqrt(3) + W
# Center-to-Center Horizontal (diag) X component = 1.5 * R + (W/cos(30))/2 ?
# Let's just use a grid generator approach provided by CadQuery `rhex` but filter points.

# Create a large grid of points and select the ones that match the shape
all_points = []
rows = 3
cols = 5
y_spacing = (math.sqrt(3) * hex_radius) + hex_wall_thickness
x_spacing = 1.5 * hex_radius + (hex_wall_thickness * math.sqrt(3)/2) # Rough approximation for x spacing logic

# Let's define the points explicitly based on the visual layout (3-4-3 or 3-3-3 pattern)
# Visual analysis:
# Center row: 3 hexes
# Upper row: 3 hexes, shifted Left relative to center
# Lower row: 3 hexes, shifted Right relative to center
# Wait, looking really closely at the image provided.
# Left side: 1 single hex? No.
# It looks like a diagonal stripe almost.
# Let's trace the "holes":
# Row 0 (Center Y):  (0,0), (+1,0), (+2,0) ... relative units
# Row +1 (Upper Y):  (-0.5, 1), (0.5, 1), (1.5, 1) ...
# Row -1 (Lower Y):  (0.5, -1), (1.5, -1), (2.5, -1) ...

# Let's try to build exactly the specific 10-hole pattern seen.
# Top Row: 3 holes
# Middle Row: 4 holes
# Bottom Row: 3 holes
# (Total 10 holes)
# Pattern is slightly skewed.
#
# Let's use basis vectors:
# u = (spacing_x, 0)  <-- Not quite, hex grid isn't orthogonal
# v = (spacing_x * cos(60), spacing_y * sin(60)) 

# Flat Topped parameters
# Width = 2*R
# Height = sqrt(3)*R
s = hex_wall_thickness
# Horizontal spacing (center to center)
dx = 1.5 * hex_radius + (s * math.sqrt(3)/2) 
# Vertical spacing (row to row)
dy = math.sqrt(3) * hex_radius + s

pts = []
# Middle Row (y=0)
pts.append((-dx * 1.5, 0)) # Left
pts.append((-dx * 0.5, 0)) # Mid-Left
pts.append((dx * 0.5, 0))  # Mid-Right
pts.append((dx * 1.5, 0))  # Right

# Top Row (shifted left, y = +dy/2)
# The hex grid staggers. For flat-topped, adjacent columns are shifted vertically.
# This implies adjacent rows are not just y-shifted, they are x-shifted too.
# If we treat them as rows:
# Top Row y = dy/2 (relative to middle staggering?)
# Actually, standard flat-top packing:
# (0,0)
# Neighbor right: Not possible with flat sides touching vertically?
# The image has flat sides on top/bottom.
# This means neighbors are strictly Left/Right? No, they mesh.
# This implies POINTY topped hexagons rotated 90 degrees? 
# No, "Flat Topped" means the top edge is horizontal.
# In the image, the top edge of the hexagon is horizontal.
# Flat-topped hexes tile in columns.
# (0,0) -> (0, H+gap)
# (1.5*R + gap_x, (H+gap)/2) 
x_step = 1.5 * hex_radius + (hex_wall_thickness * math.cos(math.radians(30)))
y_step = math.sqrt(3) * hex_radius + hex_wall_thickness

# Define grid coordinates (col, row)
# Visual Inspection of the 10 holes:
# Col 0: 1 hex (middle)
# Col 1: 2 hexes (top, bottom)
# Col 2: 2 hexes (middle, top? no looks like 1-2-1 pattern repeated)
# Let's look at the diagonal layout.
# Let's simply place coordinates manually to reconstruct the shape.
# Let's assume (0,0) is the geometric center of the plate.

# The pattern looks like this in (col, row_offset):
#      (0, 1)   (2, 1)   (4, 1)
#   (-1, 0)  (1, 0)   (3, 0)
#      (0, -1)  (2, -1)  (4, -1)
# This creates a dense packing.
# Looking at image:
# Top:    O   O   O
# Mid:  O   O   O   O
# Bot:    O   O   O 
# Total 10 holes.

# Coordinates generation
candidates = []
# Middle Row (4 items) - Centered on Y=0
# X coords roughly: -1.5, -0.5, 0.5, 1.5 (units of x_step)
candidates.append((-1.5 * x_step, -0.5 * y_step)) # Wait, shifting.
candidates.append((-0.5 * x_step, 0.5 * y_step))
candidates.append((0.5 * x_step, -0.5 * y_step))
candidates.append((1.5 * x_step, 0.5 * y_step))
# This creates a zigzag. The image has distinct rows.

# Let's try again. The image shows:
# A "Top" Line of 3 hexes.
# A "Middle" Line of 4 hexes.
# A "Bottom" Line of 3 hexes.
# But they interlock.
# Top line Y = +y_step/2
# Middle line Y = 0 ?? No, they would collide.

# Proper Trianglular Grid Logic
# Basis:
# Center (0,0)
# 6 neighbors at distance D and angles 30, 90, 150... for Pointy Topped?
# Image is Flat Topped.
# Neighbors at 0, 60, 120, 180, 240, 300 degrees.
# Dist D = sqrt(3)*R + gap.
# Let's map indices (i, j) -> Pos = i * u + j * v
# u = (D, 0)
# v = (D * cos(60), D * sin(60))

D = math.sqrt(3) * hex_radius + hex_wall_thickness
# u = (D, 0)
# v = (D * 0.5, D * 0.866)

grid_indices = [
    # Creating a diamond/rhombus patch and removing corners to match image
    # Let's try a 3x3 block relative to u, v axes.
    # (0,0), (1,0), (2,0)
    # (0,1), (1,1), (2,1)
    # (0,2), (1,2), (2,2)
    # Convert these to cartesian and see if it matches the shape.
    # Shape is elongated rectangle.
    # Maybe (0,0)..(3,0) and (0,1)..(3,1)
]

# Let's hardcode positions based on visual layout relative to plate center.
# The layout is symmetrical 180 deg.
# 10 holes total.
# Let's assume 3 rows.
# Row 0 (Top): y = +Y_OFFSET. x = -X1, 0, +X1
# Row 1 (Mid): y = 0. x = -X2, -X0, +X0, +X2 ??
# Row 2 (Bot): y = -Y_OFFSET. x = ...
# Because they interlock, Top and Bot rows align in X. Mid row is offset in X.

y_row_spacing = (math.sqrt(3) * hex_radius + hex_wall_thickness) * 0.5 * math.sqrt(3) # Vertical distance between rows in hex grid = 0.75 * height_flat_to_flat?
# In flat topped:
# Vertical distance between adjacent rows (which are offset x) is (Height/2 + Gap_y) ? 
# No. Vertical distance between centers is (sqrt(3)/2 * D_center_center).
# D_cc = sqrt(3)*R + gap.
# dy = D_cc * sin(60) = (sqrt(3)*R + gap) * sqrt(3)/2 = 1.5*R + ...
# Wait, geometry check.
# Height of hex = sqrt(3)*R.
# Stacking: Tip of one goes into "valley" of two others.
# Vertical step = Height/2 + (Height/2)/2 ? No.
# Vertical step = 0.75 * Height? No, that's for pointy topped.
# For flat topped, vertical step = Height/2 (if direct stack) or...
# Let's use the standard CadQuery hexagon packing assumption:
# It's a triangular lattice.
# Basis vector length L = sqrt(3)*R + wall.
# Row Height = L * sin(60) = L * sqrt(3)/2.

L = math.sqrt(3) * hex_radius + hex_wall_thickness
row_height = L * math.sqrt(3) / 2.0
col_width = L # Distance between centers in a horizontal row

final_points = []

# Middle Row (Center at y=0?)
# Actually, looking at the image, there is a central horizontal axis.
# On this axis, there are flat vertical edges between hexes?
# No, the hexes have flat tops.
# So the "pointy" sides point Left/Right.
# There is a zigzag interface horizontally.
#
# Let's build:
# Row 0 (Top): 3 Hexes. Center X coords: -L, 0, L. Y = +row_height/2
# Row 1 (Bottom): 3 Hexes. Center X coords: -L, 0, L. Y = -row_height/2
# Mid section: The holes mesh.
#
# Image shows:
#      H   H   H      (Top row)
#    H   H   H   H    (Middle row)
#      H   H   H      (Bottom row)
# Total 10.
#
# Coordinates relative to center:
# Row Top (y = +row_height): x = -L, 0, L
# Row Mid (y = 0): x = -1.5L, -0.5L, 0.5L, 1.5L
# Row Bot (y = -row_height): x = -L, 0, L
#
# Check overlap:
# Top (0, rh) vs Mid (0.5L, 0).
# Distance^2 = (0.5L)^2 + (rh)^2
# rh = L * sqrt(3)/2
# Dist^2 = 0.25 L^2 + 0.75 L^2 = 1.0 L^2.
# Dist = L. Perfect.
#
# So the pattern is:
# Top Row: 3 items centered at x=0
# Mid Row: 4 items centered at x=0 (so offsets +/- 0.5L, +/- 1.5L)
# Bot Row: 3 items centered at x=0

# Define parameters based on this logic
L = (math.sqrt(3) * hex_radius) + hex_wall_thickness
rh = L * math.sqrt(3) / 2.0

# Row Top
for i in [-1, 0, 1]:
    final_points.append((i * L, rh))

# Row Bot
for i in [-1, 0, 1]:
    final_points.append((i * L, -rh))

# Row Mid
for i in [-1.5, -0.5, 0.5, 1.5]:
    final_points.append((i * L, 0))

# --- Construction ---

# 1. Base Plate
base = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Hexagons
# Create a single hexagon wire (flat topped means rotation=0 in CQ usually implies pointy on x-axis?
# polygon(n, d): d is diameter of circumcircle.
# We want flat side up.
# Standard polygon(6, d) puts a vertex at (d/2, 0) -> Pointy right.
# We want Flat Top -> Pointy Right is correct? No.
# Flat top means vertex at 90 deg.
# CQ polygon starts at 0 deg (flat side vertical).
# Rotating 90 deg makes flat side horizontal (Flat Top).
# But wait, looking at the image:
# The hexagons have horizontal top and bottom edges.
# That is a "Flat Topped" hexagon.
# CQ `polygon` creates a polygon with vertex at x-axis (Pointy Right).
# To get Flat Top, we need to rotate 90 degrees.
# However, `cq.Workplane.polygon` has a `circumscribed` parameter? No.
# `polygon(sides, diameter)`
# Let's just draw one and rotate it.

cut_shape = (
    cq.Workplane("XY")
    .polygon(6, hex_radius * 2) # Diameter = 2*Radius
    .rotate((0,0,1), (0,0,0), 90) # Rotate to be flat topped
    .extrude(plate_thickness * 2) # Make sure it cuts through
)

# 3. Apply cuts
result = base.pushPoints(final_points).cutEach(lambda loc: cut_shape.val().located(loc))

# Optimization:
# Instead of cutEach with a lambda which can be slow or tricky with contexts,
# we can use the standard 2D sketch approach to subtract.

# Better approach for clean code:
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .pushPoints(final_points)
    .polygon(6, hex_radius * 2)
    .rotate((0,0,0), (0,0,1), 90) # Rotate wires in place
    .cutBlind(-plate_thickness)   # Cut through
)

# Re-verify the `rotate` chain. `rotate` on 2D stack might rotate the whole stack or individual wires?
# In CQ 2.x, `.polygon().rotate()` rotates the wires around their local centers if items on stack?
# Actually, `.polygon` puts wires on the stack. `.rotate` rotates the workplane or objects?
# Safer to define the profile first or use `each`.

# Let's use `cutBlind` directly with the correct rotation set in the polygon call? No, polygon doesn't take rotation.
# Let's use `eachpoint` pattern or just create a tool.

# Re-evaluating rotation:
# cq.Workplane("XY").polygon(6, 10).val() -> Vertex at (5,0). Flat side is vertical.
# Image has Flat side horizontal.
# So we need 90 deg rotation.

tool = (
    cq.Workplane("XY")
    .polygon(6, hex_radius * 2)
    .rotate((0,0,0), (0,0,1), 90)
    .extrude(plate_thickness)
)

# Combine points and cut
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .pushPoints(final_points)
    .cutEach(lambda loc: tool.val().located(loc))
)
# Note: cutEach expects the solid tool to be located. 
# Using .val().located(loc) moves the tool to the stack point.

# Final check on dimensions
# Width 150.
# L (spacing) ~= 1.732 * 10 + 3 ~= 20.3
# Max X extent = 1.5 * L + Radius ~= 30 + 10 = 40. Total width 80 centered.
# 150 width is plenty.
# Max Y extent = rh + Radius ~= 17 + 10 = 27. Total height 54 centered.
# 80 height is plenty.

# Code structure looks solid.