import cadquery as cq

# Parametric dimensions
post_width = 20.0
post_depth = 50.0  # Depth of the main vertical post
post_height = 400.0

# The side protrusion dimensions
plate_thickness = 5.0
plate_width = 50.0 # Protrusion length
plate_height = 80.0

# The separate floating plate dimensions
float_plate_width = 80.0
float_plate_depth = 30.0
float_plate_thickness = 5.0

# Dimensions for the cutout/step in the main post
step_depth = 10.0 # How deep the cut is
step_height_ratio = 0.7 # Where the step starts vertically
cutout_width = 2.0 # Thin slot near top

# --- Main Vertical Post Construction ---
# Create the base rectangular post
post = cq.Workplane("XY").box(post_width, post_depth, post_height)

# Create the step feature. It looks like the back part is full height, 
# but the front part stops short or is cut away.
# Let's model it as a cut on the front face.
# We cut away the top section of the front half.
cut_height = post_height * (1 - step_height_ratio)
cut_start_z = (post_height * step_height_ratio) - (post_height / 2)

# It actually looks more like two vertical planks sandwiched, with the front one shorter.
# Or a single piece with a "rabbet" cut.
# Let's assume a rabbet cut on one side (let's say +Y side).
post = post.faces(">Y").workplane().center(0, post_height/2 - cut_height/2).rect(post_width, cut_height).cutThruAll()

# There is a small slot/cutout near the top of the remaining back section.
slot_height = 40.0
slot_width = 2.0
slot_z_offset = post_height/2 - 20 - slot_height/2
post = post.faces(">X").workplane().center(post_depth/4, slot_z_offset).rect(post_depth/2, slot_width).cutThruAll()

# --- Protruding Plate (attached) ---
# This plate sticks out from the side (-X direction)
plate_z_pos = 50.0 # Vertical position
attached_plate = (
    cq.Workplane("YZ")
    .workplane(offset= -post_width/2) # Move to the left face
    .center(0, plate_z_pos)
    .rect(post_depth, plate_height)
    .extrude(-plate_width) # Extrude outwards to the left
)

# --- Floating Plate ---
# This is the separate thin plate floating in space in the image (likely an exploded view element)
float_plate_x_pos = -post_width/2 - plate_width - 20 # Gap from the attached plate
float_plate_z_pos = plate_z_pos - 20

floating_plate = (
    cq.Workplane("XY")
    .workplane(offset=float_plate_z_pos)
    .center(float_plate_x_pos, 0)
    .box(float_plate_depth, float_plate_width, float_plate_thickness)
)
# Rotate it to match the orientation in the image (flat horizontal)
# The image shows the floating piece is horizontal. 
# Re-adjusting: The attached plate is vertical. The floating one is horizontal.
# Let's redefine the floating plate construction to be cleaner.

floating_plate_final = (
    cq.Workplane("XY")
    .workplane(offset=plate_z_pos - plate_height/2) # Align with bottom of attached plate roughly
    .center(-post_width/2 - plate_width/2 - 40, 0) # Position to the left
    .box(plate_width + 20, float_plate_depth, float_plate_thickness)
)

# Refinement based on close inspection:
# The main post has a specific joint detail. It looks like a lap joint or a stepped cut.
# Let's refine the main post to be two pieces: a long back piece and a shorter front piece.

# 1. Back piece (full height)
back_piece = cq.Workplane("XY").box(post_width, post_depth/2, post_height)

# 2. Front piece (shorter, attached to the bottom)
front_piece_height = post_height * 0.75
front_piece = (
    cq.Workplane("XY")
    .center(0, -post_depth/2) # Shift so it abuts the back piece
    .box(post_width, post_depth/2, front_piece_height)
    .translate((0, 0, -(post_height - front_piece_height)/2))
)

# 3. Combine them
main_assembly = back_piece.union(front_piece)

# 4. Add the slot to the top of the back piece
main_assembly = (
    main_assembly.faces(">X")
    .workplane(centerOption="CenterOfBoundBox")
    .center(post_depth/4, post_height/2 - 40) # Position near top
    .rect(5, 40) # Slot dimensions
    .cutThruAll()
)

# 5. Side Plate (The vertical rectangular plate sticking out)
side_plate = (
    cq.Workplane("YZ")
    .workplane(offset=-post_width/2)
    .center(-post_depth/4, 20) # Align with the seam
    .rect(post_depth*0.8, 60)
    .extrude(-60)
)

# 6. Horizontal Plate (The floating one)
horiz_plate = (
    cq.Workplane("XY")
    .center(-post_width/2 - 50, -post_depth/4)
    .box(60, 30, 5)
    .translate((0, 0, 20 - 30)) # Adjust height relative to side plate
)

# Combine all parts into 'result'
# The image shows disjoint parts, so we union them into one object for the 'result' variable
# or keep them separate? CadQuery usually returns one object. Let's union them.
result = main_assembly.union(side_plate).union(horiz_plate)