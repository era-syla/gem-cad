import cadquery as cq

# --- Parametric Variables ---
# General
plate_thickness = 5.0

# Left Plate (The L-shaped one)
left_plate_width_main = 100.0
left_plate_depth_main = 120.0
left_plate_cutout_width = 50.0
left_plate_cutout_depth = 60.0
left_plate_connector_tab_width = 40.0
left_plate_connector_tab_length = 30.0

# Right Plate (The long strip)
right_plate_length = 250.0
right_plate_width_start = 60.0
right_plate_width_end = 30.0
right_plate_cutout_radius = 20.0 # Large cutout on bottom edge

# Center Block (Black connector)
block_length = 40.0
block_width = 15.0
block_height = 15.0

# Vertical Post
post_height = 80.0
post_width = 10.0
post_depth = 10.0
post_hole_dia = 5.0

# --- Geometry Construction ---

# 1. Left Plate Construction
# Start with a base rectangle
left_plate = (
    cq.Workplane("XY")
    .box(left_plate_width_main, left_plate_depth_main, plate_thickness, centered=(False, False, True))
)

# Cut out the top-right corner to make the L-shape
cutout = (
    cq.Workplane("XY")
    .box(left_plate_cutout_width, left_plate_cutout_depth, plate_thickness + 2, centered=(False, False, True))
    .translate((left_plate_width_main - left_plate_cutout_width, left_plate_depth_main - left_plate_cutout_depth, -1))
)
left_plate = left_plate.cut(cutout)

# Add the small tab connecting to the center
tab = (
    cq.Workplane("XY")
    .box(left_plate_connector_tab_length, left_plate_connector_tab_width, plate_thickness, centered=(False, False, True))
    .translate((left_plate_width_main, 0, 0))
)
left_plate = left_plate.union(tab)

# Add holes to Left Plate
left_plate = (
    left_plate.faces(">Z").workplane()
    .pushPoints([(20, 20), (20, 100), (80, 20), (110, 20), (120, 30)])
    .hole(4.0)
)

# 2. Right Plate Construction
# Define points for a custom polygon to handle the tapered shape
pts = [
    (0, 0),
    (right_plate_length, 0),
    (right_plate_length, right_plate_width_end),
    (right_plate_length - 30, right_plate_width_end), # Step up
    (right_plate_length - 30, right_plate_width_end + 10),
    (100, right_plate_width_start), # Taper start
    (0, right_plate_width_start)
]

right_plate = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(plate_thickness)
)

# Add large cutout on the bottom edge
cutout_circle = (
    cq.Workplane("XY")
    .circle(25)
    .extrude(plate_thickness + 2)
    .translate((180, 0, -1))
)
right_plate = right_plate.cut(cutout_circle)

# Add holes to Right Plate
right_plate = (
    right_plate.faces(">Z").workplane()
    .pushPoints([(20, 50), (40, 50), (80, 40), (120, 30), (160, 35), (200, 20), (230, 15), (240, 15)])
    .hole(4.0)
    .pushPoints([(100, 20)])
    .hole(12.0) # Larger hole
    .pushPoints([(150, 20)]) # Slot-like hole (approximation)
    .slot2D(20, 10, 0)
    .cutBlind(-plate_thickness)
)

# Position Right Plate
# It connects to the end of the left plate's tab area.
# Let's shift it so its origin aligns with the center block connection
right_plate = right_plate.translate((left_plate_width_main + left_plate_connector_tab_length + block_length, -20, 0))


# 3. Center Connector Block (Black part)
# Positioned between the left plate tab and the start of the right plate geometry logic
center_block = (
    cq.Workplane("XY")
    .box(block_length, block_width, block_height, centered=(False, False, True))
    .translate((left_plate_width_main + left_plate_connector_tab_length, 0, 0))
)
# Add mounting holes to block
center_block = (
    center_block.faces(">Z").workplane()
    .pushPoints([(10, block_width/2), (30, block_width/2)])
    .hole(4.0)
)

# 4. Vertical Post
# Located near the junction of left plate and block
post = (
    cq.Workplane("XY")
    .box(post_width, post_depth, post_height, centered=(True, True, False))
    .translate((left_plate_width_main + left_plate_connector_tab_length, block_width/2, 0))
)

# Hollow out the post (square tube)
post_inner = (
    cq.Workplane("XY")
    .box(post_width - 2, post_depth - 2, post_height, centered=(True, True, False))
    .translate((left_plate_width_main + left_plate_connector_tab_length, block_width/2, 0))
)
post = post.cut(post_inner)


# --- Assembly / Result ---
# Combine all parts into one object for the final result
# Note: In a real assembly we might keep them separate using cq.Assembly, 
# but for a single 'result' geometric solid, union is standard.

result = left_plate.union(right_plate).union(center_block).union(post)