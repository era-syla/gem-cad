import cadquery as cq

# --- Parameters ---
# Plate dimensions (estimated from visual proportions)
plate_length = 200.0
plate_width = 200.0
plate_thickness = 10.0

# Hole parameters
# It looks like there are countersunk holes.
# Large holes might be for mounting, small ones for alignment or smaller screws.
# Let's define a standard countersunk hole size.
hole_diameter = 6.0
csk_diameter = 12.0
csk_angle = 90.0

# Small hole parameters (there are a few tiny holes)
small_hole_diameter = 3.0
small_csk_diameter = 6.0

# --- Hole Coordinates ---
# The pattern is complex. Let's try to coordinate them relative to the center (0,0).
# The plate seems to have two main clusters of holes.
# Let's estimate coordinates based on a grid system relative to the center.
# Assuming the plate is centered at (0,0).

# Left Cluster (approximate coordinates)
# Looks like a pattern for a linear rail carriage or similar mounting block.
# Let's identify the 'left' group and 'right' group.

# The pattern looks symmetric. Let's define the right side pattern and mirror it or just list all points.
# Actually, looking closer, the two clusters are rotationally symmetric (180 degrees) around the center.
# Let's define one cluster and rotate it to get the other.

# Let's define the cluster in the "bottom-left" quadrant first, then the "top-right".
# Wait, looking at the image:
# There is a cluster in the bottom-left area.
# There is a cluster in the top-right area.
# Let's map the bottom-left cluster first.

# Bottom-Left Cluster Points (approx X, Y relative to center):
# There's a set of 4 inner holes forming a small rectangle.
# There's a set of outer holes.

# Let's guess some reasonable engineering dimensions.
# Center-to-center spacing looks like 20mm, 30mm, etc.

# Let's define the "Right" cluster first (positive X usually)
# Actually, let's just list the estimated coordinates for the distinct holes.
# Looking at the image orientation:
# X axis runs bottom-left to top-right of the plate face.
# Y axis runs top-left to bottom-right of the plate face.
# (Standard isometric view assumption).

# Let's assume standard Cartesian coordinates on the face:
# Center is (0,0).
# Let's trace the "Top Right" group (positive X, positive Y mostly).
top_right_group = [
    (20, 20),   # Inner square corner
    (40, 20),   # Inner square corner
    (20, 40),   # Inner square corner
    (40, 40),   # Inner square corner
    (10, 60),   # Outer arc
    (30, 70),   # Outer arc
    (60, 50),   # Outer arc
    (75, 25),   # Outer arc
    (65, 0),    # Near centerline
]

# Let's re-examine the image pattern carefully.
# It looks like mounting plates for two identical components.
# Let's try to identify the specific pattern. It looks like a standard mounting pattern for MGN linear rail blocks or similar, but doubled.

# Let's list coordinates manually based on visual grid estimation.
# Assume plate is 100x100 units for coordinate estimation.
# Let's say coordinates are (x, y).

# Group 1 (Lower Left / Front Left)
# Inner rectangle 1:
p1_inner = [
    (-20, -15), (-40, -15),
    (-20, -35), (-40, -35)
]
# Surrounding holes for Group 1:
p1_outer = [
    (-60, -15), # Far left
    (-60, -45), # Far left lower
    (-50, -65), # Bottom left corner-ish
    (-20, -75), # Bottom edge
    (10, -55),  # Towards center
    (0, -25)    # Near center
]
# Small hole
p1_small = [(-75, -10), (-10, -85)] # Just guessing location of tiny dots

# This is getting messy. Let's try a more structured approach.
# The pattern consists of standard holes.
# Let's assume the plate is 200x200.
# Let's define the list of all standard hole centers (x, y).

standard_holes = []
small_holes = []

# Analyzing symmetries:
# The pattern in the lower-left seems to be rotated 180 degrees to form the upper-right pattern.
# Let's build the lower-left pattern relative to a local center, say (-50, -50).
# But it looks more like a single complex pattern for a specific machine part (e.g. 3D printer bed carriage).

# Let's estimate coordinates directly from visual grid (0 to 10 scale).
# Plate corners: (-10, -10) to (10, 10).
# Group 1 (Bottom Left quadrant):
#   - Row 1 (y ~ -2): x ~ -2, -4
#   - Row 2 (y ~ -4): x ~ -2, -4
#   - Outliers: x~ -6, y~ -2; x~ -6, y~ -5; x~ -2, y~ -7; x~ -5, y~ -7; x~ 0, y~ -3; x~ 0, y~ -6;
#   - Small hole: x~ -8, y~ -1; x~ -1, y~ -8

# Let's translate these to mm assuming a 20mm grid spacing.
grid = 20.0
# Lower Left Group (Shifted by approx -10, -10 relative to grid)
g1_centers = [
    # The central 4-hole rectangular pattern
    (-1.0 * grid, -1.0 * grid), 
    (-2.0 * grid, -1.0 * grid),
    (-1.0 * grid, -2.0 * grid),
    (-2.0 * grid, -2.0 * grid),
    
    # The peripheral holes
    (-3.0 * grid, -1.0 * grid), # Leftmost top
    (-3.5 * grid, -2.5 * grid), # Leftmost mid
    (-3.0 * grid, -3.5 * grid), # Leftmost bot
    (-1.0 * grid, -3.5 * grid), # Bottom mid
    (0.0 * grid, -2.5 * grid),  # Right mid
    (0.0 * grid, -1.5 * grid)   # Right top
]

# That doesn't look quite right compared to the image.
# Let's refine the "grid".
# The four central holes in the lower-left group form a square or slight rectangle.
# Let's place the center of this group at (-50, -50).
# Inner 4 holes: (+-10, +-10) relative to group center.
#   -> (-40, -40), (-60, -40), (-40, -60), (-60, -60)
# Looking at image:
#   Front-left cluster:
#   Two holes aligned horizontally.
#   Two holes below them aligned horizontally.
#   This forms a square.
#   To the left of the square, two holes vertically aligned.
#   Below the square, two holes horizontally aligned.
#   To the right of the square, maybe one hole?

# Final Selection of Coordinates (Visual Approximation)
# Let's work with the whole plate coordinate system directly.
# Axis: X (horizontal in screen), Y (vertical in screen effectively).
# Let's assume the plate is 150mm x 150mm.

# --- LOWER LEFT CLUSTER ---
# Inner Square
h1 = (-30, -30)
h2 = (-50, -30)
h3 = (-30, -50)
h4 = (-50, -50)

# Left Flank
h5 = (-70, -40)
h6 = (-65, -60) # Slightly staggered

# Bottom Flank
h7 = (-40, -70)
h8 = (-20, -65)

# Center-ward Flank
h9 = (-10, -40)
h10 = (0, -20) # This one is quite central

# --- UPPER RIGHT CLUSTER ---
# Rotational symmetry of Lower Left (x -> -x, y -> -y)
# Inner Square
h11 = (30, 30)
h12 = (50, 30)
h13 = (30, 50)
h14 = (50, 50)

# Right Flank (mirror of Left Flank)
h15 = (70, 40)
h16 = (65, 60)

# Top Flank (mirror of Bottom Flank)
h17 = (40, 70)
h18 = (20, 65)

# Center-ward Flank
h19 = (10, 40)
h20 = (0, 20)

# Small alignment holes
# Bottom left extreme
s1 = (-60, -20) # Not quite, looking at the image it's far left. Let's say (-80, -20)
s2 = (-20, -80) # Far bottom
# Top right extreme (symmetric)
s3 = (80, 20)
s4 = (20, 80)

# Merging lists
# Based on the image, let's refine the specific positions to look aesthetically identical.
# The image shows two distinct groups.
# Group 1 (Bottom Left):
#   - A square of 4 holes.
#   - A pair to the left.
#   - A pair below.
#   - One towards the middle-right.
#   - One towards the middle-top.

# Let's build coordinate lists.
main_hole_coords = [
    # -- Group Bottom-Left --
    # The Square
    (-25, -25), (-45, -25),
    (-25, -45), (-45, -45),
    # Left side
    (-65, -35), (-60, -55),
    # Bottom side
    (-35, -65), (-55, -60), # Swapped slightly for visual match
    # Towards center
    (-10, -30), # Near horizontal center line
    (-30, -10), # Near vertical center line
    
    # -- Group Top-Right (Rotated 180) --
    # The Square
    (25, 25), (45, 25),
    (25, 45), (45, 45),
    # Right side
    (65, 35), (60, 55),
    # Top side
    (35, 65), (55, 60),
    # Towards center
    (10, 30),
    (30, 10),
]

# Adjusting for visual accuracy:
# The "Towards center" holes in the image:
# In the bottom-left group, there is a hole roughly at the same Y as the top row of the square, but further right.
# And a hole roughly at the same X as the right column of the square, but further up.
# My coords (-10, -30) and (-30, -10) cover this reasonable well.

# Small holes
# There is a small hole to the far left of the top row of the bottom-left square.
# There is a small hole to the far bottom of the right column of the bottom-left square.
small_hole_coords = [
    (-80, -25),  # Left of bottom-left group
    (-25, -80),  # Below bottom-left group
    (80, 25),    # Right of top-right group (symmetry)
    (25, 80),    # Above top-right group (symmetry)
]

# Create the base plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Add main countersunk holes
result = (result.faces(">Z").workplane()
          .pushPoints(main_hole_coords)
          .cskHole(hole_diameter, csk_diameter, csk_angle))

# Add small countersunk holes
result = (result.faces(">Z").workplane()
          .pushPoints(small_hole_coords)
          .cskHole(small_hole_diameter, small_csk_diameter, csk_angle))
