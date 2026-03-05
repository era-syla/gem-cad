import cadquery as cq

# Parametric Dimensions
plate_width = 180.0
plate_height = 180.0
plate_thickness = 30.0
corner_radius = 20.0

# Central Cutout
center_hole_size = 60.0

# Peripheral Cutouts (4 rectangular holes)
rect_hole_width = 50.0
rect_hole_height = 35.0
rect_hole_offset_x = 45.0  # Center-to-center offset from origin
rect_hole_offset_y = 55.0  # Center-to-center offset from origin

# Small Screw Holes
screw_hole_diameter = 3.0
screw_hole_pattern_offset_x = 75.0 # Outer pattern width/2
screw_hole_pattern_offset_y = 75.0 # Outer pattern height/2
inner_screw_offset_x = 35.0 # Inner vertical holes offset
inner_screw_offset_y = 35.0 # Inner horizontal holes offset

# 1. Base Plate
# Create a centered rectangle and extrude it
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
)

# 2. Round the corners (Fillet)
# Select edges parallel to Z axis
result = base.edges("|Z").fillet(corner_radius)

# 3. Create the Central Square Cutout
result = (
    result.faces(">Z")
    .workplane()
    .rect(center_hole_size, center_hole_size)
    .cutBlind(-plate_thickness)
)

# 4. Create the Four Rectangular Cutouts
# We define centers relative to the origin
cutout_centers = [
    (rect_hole_offset_x, rect_hole_offset_y),
    (-rect_hole_offset_x, rect_hole_offset_y),
    (-rect_hole_offset_x, -rect_hole_offset_y),
    (rect_hole_offset_x, -rect_hole_offset_y),
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(cutout_centers)
    .rect(rect_hole_width, rect_hole_height)
    .cutBlind(-plate_thickness)
)

# 5. Create Small Screw Holes
# Analyzing the image, there seems to be a specific pattern:
# - Corners
# - Mid-points near the outer edge
# - Points near the inner cutouts
# Let's define a list of coordinates for all the small holes based on visual estimation.

small_hole_locations = [
    # Top edge row
    (-screw_hole_pattern_offset_x, screw_hole_pattern_offset_y), 
    (0, screw_hole_pattern_offset_y), 
    (screw_hole_pattern_offset_x, screw_hole_pattern_offset_y),
    
    # Bottom edge row
    (-screw_hole_pattern_offset_x, -screw_hole_pattern_offset_y), 
    (0, -screw_hole_pattern_offset_y), 
    (screw_hole_pattern_offset_x, -screw_hole_pattern_offset_y),
    
    # Left edge middle
    (-screw_hole_pattern_offset_x, 0),
    
    # Right edge middle
    (screw_hole_pattern_offset_x, 0),

    # Inner holes (surrounding the central cutout/between rect cutouts)
    # Top inner
    (-inner_screw_offset_x, 50), # Approximate Y location based on rect hole
    (inner_screw_offset_x, 50),
    
    # Bottom inner
    (-inner_screw_offset_x, -50),
    (inner_screw_offset_x, -50),
]

# Additional mid-points on the sides based on image inspection
# It looks like there are holes vertically aligned with the outer rect holes
side_holes = [
    (-75, 25), (-75, -25), # Left side extras
    (75, 25), (75, -25)    # Right side extras
]

# Refined list based strictly on the visible symmetric pattern in the image:
# 4 corners, 4 mid-sides (top/bottom/left/right), and 8 inner points near the rect cutouts.
final_hole_points = [
    # Outer Loop
    (-75, 75), (0, 80), (75, 75),  # Top row (middle one slightly higher/lower usually, assuming alignment here)
    (-80, 0), (80, 0),             # Middle sides
    (-75, -75), (0, -80), (75, -75), # Bottom row

    # Inner/Middle mechanics holes (near the rectangular cutouts)
    (-25, 75), (25, 75),           # Top edge inner pair
    (-25, -75), (25, -75),         # Bottom edge inner pair
    
    (-75, 35), (-75, -35),         # Left edge inner pair
    (75, 35), (75, -35),           # Right edge inner pair
]

# Looking closer at the image, the pattern is:
# Outer perimeter: Top/Bottom have 4 holes each. Left/Right have 3 holes each (corners shared).
# Actually, let's look at the specific hole placement relative to the features.
# It seems there is a hole at every corner of the plate (inside the radius),
# and holes aligned with the "ribs" between cutouts.

holes = []

# Corner holes
dx = 72.0
dy = 72.0
holes.extend([(dx, dy), (-dx, dy), (-dx, -dy), (dx, -dy)])

# Mid-edge holes (aligned with center axes)
holes.extend([(0, 82), (0, -82), (82, 0), (-82, 0)])

# Holes near the rectangular cutouts (top/bottom ribs)
holes.extend([(30, 82), (-30, 82), (30, -82), (-30, -82)])

# Holes near the rectangular cutouts (left/right ribs)
holes.extend([(82, 30), (82, -30), (-82, 30), (-82, -30)])


result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(holes)
    .hole(screw_hole_diameter)
)