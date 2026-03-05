import cadquery as cq

# --- Parameters ---
# Overall dimensions estimation based on typical stepper motor mount proportions
plate_thickness = 5.0

# Bounding box width/height estimates
overall_width = 80.0
overall_height = 60.0

# Right arm dimensions
right_arm_width = 20.0
right_arm_height = 40.0  # From bottom of the central cutout
right_arm_top_y = 30.0   # Relative to center

# Left arm dimensions
left_arm_width = 15.0
left_arm_height = 25.0
left_arm_top_y = 15.0

# Bottom section
bottom_height = 20.0
bottom_tab_drop = 10.0 # The extra bit hanging down on the left-ish side

# Central Cutout (U-shape)
cutout_center_x = 0.0
cutout_width = 25.0
cutout_depth = 15.0

# Mounting Holes (M3/M4/M5 approximations)
small_hole_diam = 3.5  # M3 clearance
large_hole_diam = 5.5  # M5 clearance

# Fillet radius
fillet_radius = 2.0

# --- Geometry Construction ---

# We will define the profile using a sketch/polyline approach.
# Let's establish a coordinate system where (0,0) is roughly the center of the main U-cutout.

# Points for the outer contour (counter-clockwise starting from top-left of the left arm)
# Let's adjust coordinates to make sense visually.
# Center of the U-cutout circle is at (0,0).

# Define key x-coordinates
x_cutout_left = -10.0
x_cutout_right = 10.0
x_left_arm_outer = -40.0
x_left_arm_inner = -15.0 
x_right_arm_inner = 15.0
x_right_arm_outer = 40.0

# Define key y-coordinates
y_top_right = 35.0
y_top_left = 15.0
y_bottom_main = -25.0
y_bottom_tab = -35.0
y_cutout_bottom = -5.0

# Let's refine the shape logic. It looks like a union of rectangles or a single polygon.
# Let's try to build it as a single base shape and then subtract/add features.

# Base shape construction
# Create the main body
base = (
    cq.Workplane("XY")
    .moveTo(x_left_arm_outer, y_top_left)
    .lineTo(x_left_arm_inner, y_top_left)
    # The small dip before the U-cutout
    .lineTo(x_left_arm_inner, 0) 
    .lineTo(x_cutout_left, 0)
    # The U-cutout
    .threePointArc((0, y_cutout_bottom), (x_cutout_right, 0))
    # Right side of cutout
    .lineTo(x_right_arm_inner, 0)
    .lineTo(x_right_arm_inner, y_top_right)
    .lineTo(x_right_arm_outer, y_top_right)
    .lineTo(x_right_arm_outer, y_bottom_main) # Right edge down
    # Bottom edge with the step
    .lineTo(x_left_arm_inner, y_bottom_main)
    .lineTo(x_left_arm_inner, y_bottom_tab) # Step down
    .lineTo(x_left_arm_outer, y_bottom_tab) # Left bottom
    .close()
    .extrude(plate_thickness)
)

# Apply fillets to vertical edges
result = base.edges("|Z").fillet(fillet_radius)

# --- Holes ---

# Coordinates estimation
# Left arm holes (small)
hole_left_top = (-32.0, 10.0)
hole_left_mid = (-32.0, -15.0) # Actually looks like there are two on the left column

# The image shows:
# Left side: 2 small holes vertically aligned
# Right side: 2 small holes vertically aligned
# Bottom center area: 2 larger holes

# Refined coordinates
h_left_x = -32.5
h_right_x = 32.5
h_top_y_left = 8.0
h_bot_y_left = -18.0
h_top_y_right = 28.0
h_bot_y_right = 2.0 # Roughly aligned with the cutout center

h_large_y = -18.0
h_large_x_left = -15.0
h_large_x_right = 20.0 

# Create holes
result = (
    result
    # Left small holes
    .faces(">Z").workplane()
    .pushPoints([(h_left_x, h_top_y_left), (h_left_x, h_bot_y_left)])
    .hole(small_hole_diam)
    # Right small holes
    .pushPoints([(h_right_x, h_top_y_right), (h_right_x, h_bot_y_right)])
    .hole(small_hole_diam)
    # Large bottom holes
    .pushPoints([(h_large_x_left, -28.0), (h_large_x_right, -15.0)]) # Adjusted based on visual scan
)

# Re-evaluating large hole positions based on image
# The left large hole is on the tab that hangs down.
# The right large hole is on the main body.
result = (
    base
    .edges("|Z").fillet(fillet_radius)
    .faces(">Z").workplane()
    # Left column small holes
    .pushPoints([(-33, 5), (-33, -20)])
    .hole(small_hole_diam)
    # Right column small holes
    .pushPoints([(33, 28), (33, 2)])
    .hole(small_hole_diam)
    # Large hole on the bottom left tab
    .pushPoints([(-18, -28)])
    .hole(large_hole_diam)
    # Large hole on the bottom right area
    .pushPoints([(18, -15)])
    .hole(large_hole_diam)
)