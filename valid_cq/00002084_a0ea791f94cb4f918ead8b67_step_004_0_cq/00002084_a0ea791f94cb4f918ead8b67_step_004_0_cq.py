import cadquery as cq

# --- Parameter Definitions ---
# Overall plate dimensions
plate_width = 150.0   # Total width (X)
plate_height = 150.0  # Total height (Y)
plate_thickness = 20.0 # Total thickness (Z)
corner_radius = 15.0  # Radius of the main plate corners

# Central cutout dimensions
center_hole_size = 50.0 

# Peripheral rectangular cutouts (4 symmetrical holes)
# Judging by image, they are wider than they are tall
rect_hole_width = 45.0
rect_hole_height = 25.0
# Distance from center to the center of these rectangular holes
rect_hole_offset_x = 35.0
rect_hole_offset_y = 45.0

# Small mounting holes
mount_hole_diameter = 3.0
# These holes seem to be arranged around the perimeter and near the cutouts.
# Let's define a pattern based on the image visual estimation.
# Outer ring pattern
outer_hole_inset = 8.0 # Distance from edge
outer_w = plate_width/2 - outer_hole_inset
outer_h = plate_height/2 - outer_hole_inset

# Inner/Mid holes locations - trying to match the specific layout in the image
# It looks like there are holes between the cutouts and on the sides.
mid_hole_y_offset = 20.0
mid_hole_x_offset = 65.0 

# --- Modeling ---

# 1. Create the base plate with rounded corners
base_plate = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Cut the central square hole
result = (
    base_plate
    .faces(">Z")
    .workplane()
    .rect(center_hole_size, center_hole_size)
    .cutThruAll()
)

# 3. Cut the 4 surrounding rectangular holes
# We use pushPoints to place them symmetrically
rect_hole_centers = [
    (rect_hole_offset_x, rect_hole_offset_y),
    (-rect_hole_offset_x, rect_hole_offset_y),
    (rect_hole_offset_x, -rect_hole_offset_y),
    (-rect_hole_offset_x, -rect_hole_offset_y)
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(rect_hole_centers)
    .rect(rect_hole_width, rect_hole_height)
    .cutThruAll()
)

# 4. Drill the small mounting holes
# Based on the image, there is a distinct pattern of small holes.
# Let's define the coordinates explicitly to match the visual pattern.

hole_locations = []

# Corners (approximate locations based on visual inspection)
# Top Row
hole_locations.append((-outer_w + 10, outer_h)) 
hole_locations.append((0, outer_h))
hole_locations.append((outer_w - 10, outer_h))

# Bottom Row
hole_locations.append((-outer_w + 10, -outer_h))
hole_locations.append((0, -outer_h))
hole_locations.append((outer_w - 10, -outer_h))

# Side Columns (left and right edges)
hole_locations.append((-outer_w, outer_h - 25))
hole_locations.append((-outer_w, 0))
hole_locations.append((-outer_w, -outer_h + 25))

hole_locations.append((outer_w, outer_h - 25))
hole_locations.append((outer_w, 0))
hole_locations.append((outer_w, -outer_h + 25))

# Inner holes near the rectangular cutouts (top/bottom)
hole_locations.append((0, rect_hole_offset_y + rect_hole_height/2 + 5)) # Above top rects (center) - actually looking closer, there isn't one there in the image
# Let's refine based on the specific image:
# There appear to be holes framing the rectangular cutouts vertically.

specific_hole_pattern = [
    # Top edge row
    (-55, 65), (0, 65), (55, 65),
    # Bottom edge row
    (-55, -65), (0, -65), (55, -65),
    # Left edge column
    (-65, 55), (-65, 0), (-65, -55),
    # Right edge column
    (65, 55), (65, 0), (65, -55),
    # Inner holes (top/bottom of center square) - none visible immediately adjacent
    # Holes adjacent to outer rects
    (-35, 65), (35, 65), # Duplicate of top row slightly adjusted
]

# Let's stick to a simpler, symmetrical grid that closely approximates the visual:
clean_hole_locations = [
    # Top Edge
    (-50, 67), (0, 67), (50, 67),
    # Bottom Edge
    (-50, -67), (0, -67), (50, -67),
    # Left Edge
    (-67, 50), (-67, 0), (-67, -50),
    # Right Edge
    (67, 50), (67, 0), (67, -50),
    # Inner vertical separation (between rectangles)
    (0, 35), (0, -35) 
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(clean_hole_locations)
    .hole(mount_hole_diameter)
)

# Optional: Add small fillets to the internal cutouts if desired (not strictly visible but common)
# result = result.edges("|Z").fillet(1.0) # Commented out to match the sharp edges in image