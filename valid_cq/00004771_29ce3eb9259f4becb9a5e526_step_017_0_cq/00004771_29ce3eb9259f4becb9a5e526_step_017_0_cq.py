import cadquery as cq

# Parametric dimensions
plate_width = 100.0   # Total width of the plate
plate_height = 100.0  # Total height of the plate
thickness = 3.0       # Thickness of the plate
corner_radius = 5.0   # Fillet radius for the corners

# Hole parameters
small_hole_dia = 3.2  # Diameter for the smaller, more numerous holes (e.g., for M3)
large_hole_dia = 5.0  # Diameter for the larger mounting holes (e.g., for M5)

# Pattern spacing parameters
# Based on typical grid plates (like OpenBuilds or similar V-slot gantries),
# the spacing is usually 20mm or 10mm.
# Let's deduce the grid based on visual observation.
# The plate looks roughly square.
# There is a central cross of holes.
# There are angled patterns.

# Let's define the positions manually based on the visual symmetry.
# The plate has symmetry across X and Y axes (mostly).

# List of hole coordinates (x, y) and their type ('small' or 'large')
# Assuming origin is at the center of the plate (0,0)

holes = []

# --- Central Cross Pattern (Small Holes) ---
# Vertical line
holes.append({'pos': (0, 10), 'size': 'small'})
holes.append({'pos': (0, 20), 'size': 'small'})
holes.append({'pos': (0, -10), 'size': 'small'})
holes.append({'pos': (0, -20), 'size': 'small'})
# Horizontal line (implied by the X shape but center is empty in some designs, let's look closer)
# Actually, looking at the image, there isn't a simple cross. It's more of a V-slot gantry plate layout.
# Let's mimic a generic gantry plate layout.

# Typically these have wheel mounting holes (large, usually eccentric spacers fit here)
# and component mounting holes (small).

# Let's rebuild the coordinate list based on rows/columns logic visually.

# Large holes (likely for wheels)
# Top row
holes.append({'pos': (30, 35), 'size': 'large'})
holes.append({'pos': (20, 40), 'size': 'large'})
holes.append({'pos': (10, 42.5), 'size': 'large'}) # Slightly arched

# Bottom row (mirrored)
holes.append({'pos': (30, -35), 'size': 'large'})
holes.append({'pos': (20, -40), 'size': 'large'})
holes.append({'pos': (10, -42.5), 'size': 'large'})

# Side large holes (right side)
holes.append({'pos': (35, 20), 'size': 'large'})
holes.append({'pos': (35, 0), 'size': 'large'}) # Middle right
holes.append({'pos': (35, -20), 'size': 'large'})

# It looks like the image is a standard "Universal Gantry Plate".
# Let's approximate the specific hole locations from the image logic more generally to ensure a good result.

pts_small = []
pts_large = []

# -- Large Holes (approximate locations based on typical 20-80mm gantry plates) --
# The top arc of large holes
pts_large.extend([
    (20, 42), (30, 45), (40, 48)  # Top right-ish area, actually let's just stick to the image look
])

# Let's use a more programmatic approach to replicate the visual density.

# 1. Top and Bottom Arcs (Large holes)
# Looking at the top right quadrant:
pts_large.append((35, 38))
pts_large.append((25, 42))
pts_large.append((15, 44))

# Mirrored to bottom right
pts_large.append((35, -38))
pts_large.append((25, -42))
pts_large.append((15, -44))

# 2. Right Side Vertical (Large holes)
pts_large.append((40, 20))
pts_large.append((40, 10)) # Maybe
pts_large.append((40, -10)) # Maybe
pts_large.append((40, -20))

# Actually, let's look at the specific distinctive patterns.
# There is a diagonal line of small holes.
# There is a central diamond/cross pattern.

# Let's define a clean set of coordinates that matches the visual density.

# --- Corrected Coordinate Map Estimation ---

# Set 1: The outer large holes (for V-wheels)
# Top Row
pts_large.append((20, 38))
pts_large.append((30, 42))
pts_large.append((40, 45)) 

# Bottom Row
pts_large.append((20, -38))
pts_large.append((30, -42))
pts_large.append((40, -45))

# Set 2: The small mounting holes grid
# It looks like a grid of 10mm or 20mm spacing, rotated or shifted.
# Let's generate a grid and filter, or just place explicitly.

# Explicit Placement for small holes (Left side heavy, center)
# Center vertical column
pts_small.append((0, 10))
pts_small.append((0, 20))
pts_small.append((0, -10))
pts_small.append((0, -20))

# Inner diagonals
pts_small.append((10, 10))
pts_small.append((10, -10))
pts_small.append((-10, 10))
pts_small.append((-10, -10))

# Left side array
pts_small.append((-20, 0))
pts_small.append((-20, 20))
pts_small.append((-20, -20))
pts_small.append((-30, 10))
pts_small.append((-30, -10))
pts_small.append((-30, 30))
pts_small.append((-30, -30))
pts_small.append((-40, 0))
pts_small.append((-40, 20))
pts_small.append((-40, -20))

# Top/Bottom edges small holes
pts_small.append((-10, 40))
pts_small.append((0, 40))
pts_small.append((-10, -40))
pts_small.append((0, -40))
pts_small.append((-20, 35))
pts_small.append((-20, -35))

# Specific features from image:
# 1. Top edge: 3 small holes descending left, then large holes rising right.
# 2. Bottom edge: mirrored.

# Let's refine the lists to be cleaner based on visual "zones"

final_small_holes = []
final_large_holes = []

# --- Zone 1: The Top Edge ---
# Left to Right
final_small_holes.append((-35, 32))
final_small_holes.append((-25, 36))
final_small_holes.append((-15, 39))
final_small_holes.append((-5, 41))
# Transition to large
final_large_holes.append((15, 43))
final_large_holes.append((25, 38)) # Lower
final_large_holes.append((35, 33)) # Even Lower

# --- Zone 2: The Bottom Edge (Mirror of Top) ---
final_small_holes.append((-35, -32))
final_small_holes.append((-25, -36))
final_small_holes.append((-15, -39))
final_small_holes.append((-5, -41))
# Transition to large
final_large_holes.append((15, -43))
final_large_holes.append((25, -38))
final_large_holes.append((35, -33))

# --- Zone 3: The Right Side Vertical ---
final_large_holes.append((35, 15))
final_large_holes.append((30, 5)) # Slightly inset?
final_large_holes.append((35, -15)) # 

# --- Zone 4: The Center Pattern (Small holes) ---
# Central Cross
final_small_holes.append((0, 5))
final_small_holes.append((0, 15))
final_small_holes.append((0, -5))
final_small_holes.append((0, -15))

# Diagonals around center
final_small_holes.append((10, 10))
final_small_holes.append((10, -10))
final_small_holes.append((-10, 10))
final_small_holes.append((-10, -10))

# --- Zone 5: The Left Side Pattern (Small holes) ---
final_small_holes.append((-20, 0))
final_small_holes.append((-20, 20))
final_small_holes.append((-20, -20))

final_small_holes.append((-30, 10))
final_small_holes.append((-30, -10))

final_small_holes.append((-40, 0)) # Far left center


# Create the base plate
base_plate = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Drill the small holes
plate_with_small_holes = (
    base_plate
    .faces(">Z")
    .workplane()
    .pushPoints(final_small_holes)
    .hole(small_hole_dia)
)

# Drill the large holes
result = (
    plate_with_small_holes
    .faces(">Z")
    .workplane()
    .pushPoints(final_large_holes)
    .hole(large_hole_dia)
)