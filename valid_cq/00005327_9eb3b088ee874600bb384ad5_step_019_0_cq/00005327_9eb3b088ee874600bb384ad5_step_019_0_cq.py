import cadquery as cq

# -- Parameters --
# Overall plate dimensions (estimated from visual proportions)
plate_width = 150.0
plate_height = 100.0
plate_thickness = 15.0

# Hole pattern geometry
# Estimating coordinates relative to the center of the plate (0,0)
# The image shows a pattern of holes. Let's approximate their positions.
# It looks like a mounting plate for a specific component (possibly a motor or a linear rail carriage).

# Small mounting holes (approx 4-5mm diameter)
small_hole_dia = 5.0
small_hole_cb_dia = 8.0  # Counterbore diameter (visual guess, though could be simple holes)
small_hole_cb_depth = 3.0 # Counterbore depth

# Large main hole (offset to the right)
large_hole_dia = 16.0
large_hole_cb_dia = 25.0
large_hole_cb_depth = 8.0
large_hole_x = 35.0
large_hole_y = 15.0

# Coordinates for small holes based on visual grid estimation
# Let's assume the origin is at the center of the plate
hole_locations = [
    # Left columnish
    (-50, -25), 
    (-35, 15), 
    
    # Middle diagonal-ish
    (-20, -10),
    (10, 5),
    
    # Bottom
    (0, -35),
    
    # Near large hole
    (20, 10), # Close to large hole, left
    (55, 10), # Right of large hole
    (35, 35), # Above large hole (top one)
    (35, 25), # Above large hole (lower one)
    (35, -5), # Below large hole
]

# Refined positions to match image more closely:
# The image shows:
# - A hole bottom left area
# - A hole mid-left
# - A hole bottom center
# - A diagonal line of 3 holes rising towards the large hole
# - Several holes surrounding the large hole

# Let's build the solid
# 1. Base Plate
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. The Large Counterbored Hole
# It sits to the right of the centerline and slightly up.
large_hole_pos = (25, 10)  # Adjusted estimation

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([large_hole_pos])
    .cboreHole(large_hole_dia, large_hole_cb_dia, large_hole_cb_depth)
)

# 3. The Smaller Holes
# Looking at the image, there seem to be distinct groups.
# Let's define specific coordinates that mimic the layout.

# Group 1: Far left
# One low, one mid-high
group1 = [(-55, -20), (-40, 10)]

# Group 2: Center diagonal line
# Bottom center, moving up-right
group2 = [(-10, -35), (-20, -10), (10, 0)]

# Group 3: Surrounding the large hole
# Top, bottom, right
group3 = [(25, 30), (25, -10), (50, 10)]

# Group 4: Specifically close to the large hole (maybe mounting pattern)
# There is a small hole very close above the large one
group4 = [(25, 22)] 

all_small_holes = group1 + group2 + group3 + group4

# Create the small holes. 
# Visual inspection suggests they might just be through holes or slightly chamfered.
# We will make them simple through holes for robustness.
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(all_small_holes)
    .hole(small_hole_dia)
)

# Optional: Add small chamfer to edges for realism
result = result.edges("|Z").chamfer(1.0)