import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the visual proportions
panel_width = 3000.0  # Total width of the fence section
panel_height = 1800.0 # Total height of the fence section
post_diameter = 120.0 # Diameter of the vertical posts
post_height = 2000.0  # Height of the posts (slightly taller than panel for ground embedment, or just flush)
board_thickness = 25.0 # Thickness of the horizontal boards
board_height = 200.0   # Height of a individual board
board_overlap = 0.0    # Overlap between boards (looks like tongue & groove or just stacked)
                       # The image shows distinct horizontal lines, suggesting separate boards or grooves.
                       # Let's model it as a stack of boards.
num_boards = 8         # Number of horizontal boards visible

# Recalculate board height based on total panel height if needed, 
# but let's stick to explicit dimensions for a parametric approach.
# Adjusting panel_height to fit boards exactly for cleaner geometry
panel_height = num_boards * board_height 
post_height = panel_height + 100.0 # Make posts slightly taller

# --- Geometry Construction ---

# 1. Create the vertical posts
# We'll create one post and mirror/translate it.
# The post is a cylinder.
post = cq.Workplane("XY").circle(post_diameter / 2).extrude(post_height)

# 2. Create the groove in the post for the boards
# The boards need to slot into the posts.
groove_depth = post_diameter * 0.3
groove_width = board_thickness + 2.0 # Tolerance
groove = (
    cq.Workplane("XY")
    .rect(groove_width, post_diameter) # Rectangle covering the diameter
    .extrude(panel_height)
    .translate((0, groove_depth/2, panel_height/2)) # Position it
)

# However, looking at the image, the posts seem to be halved or flattened on the inside, 
# or the boards just go into a central slot.
# Let's assume a central slot.
# Actually, the image shows the post as a full round shape on the outside.
# Let's stick to the slot idea.
# We need to cut the groove out of the post.
# To orient the slot correctly, let's assume the fence runs along the X axis.
# The post is vertical (Z). The slot should face the other post.

# Left Post
left_post = post.translate((-panel_width/2, 0, 0))
# Slot for left post (facing positive X)
left_slot = (
    cq.Workplane("XY")
    .rect(post_diameter, board_thickness) # Cut fully through to center
    .extrude(panel_height)
    .translate((-panel_width/2 + post_diameter/2, 0, panel_height/2))
)
# Actually, a simpler way is just to place the boards and combine everything later,
# but for a realistic model, the posts surround the board ends.

# Let's refine the post shape. In the image, the posts look like they might be
# slightly taller than the top board, and rounded at the top.
left_post = (
    cq.Workplane("XY")
    .circle(post_diameter / 2)
    .extrude(post_height)
    .faces(">Z").fillet(post_diameter/10) # Slight rounding on top cap
    .translate((-panel_width/2, 0, 0))
)

right_post = (
    cq.Workplane("XY")
    .circle(post_diameter / 2)
    .extrude(post_height)
    .faces(">Z").fillet(post_diameter/10)
    .translate((panel_width/2, 0, 0))
)


# 3. Create the horizontal boards
# We will create one board and stack them.
# The boards span between the centers of the posts.
board_length = panel_width - post_diameter * 0.2 # Slight overlap into post

# Profile of a single board. 
# Looking at the left edge of the image, the boards have a slight profile, 
# possibly a chamfer on top or a tongue-and-groove look (V-joint).
# Let's add a V-groove effect.

def create_board(height, thickness, length):
    # Cross-section in YZ plane
    pts = [
        (thickness/2, 0),
        (thickness/2, height - 5), # Top front chamfer start
        (thickness/2 - 2, height), # Top front edge
        (-thickness/2 + 2, height),# Top back edge
        (-thickness/2, height - 5),# Top back chamfer start
        (-thickness/2, 0)
    ]
    # Simple rectangle for now is safer and robust, adding a chamfer feature 
    # to the top edge of the extrude is easier.
    
    b = (
        cq.Workplane("XY")
        .box(length, thickness, height)
    )
    
    # Add chamfers to create the "plank" look separation
    # We select the top edges running along X
    b = b.edges("|X").filter_by(cq.Axis.Z).chamfer(3.0)
    return b

# Generate stack of boards
boards = cq.Workplane("XY")

for i in range(num_boards):
    # Elevation of the current board
    z_pos = (i * board_height) + (board_height / 2)
    
    # Create board
    current_board = (
        cq.Workplane("XY")
        .box(board_length, board_thickness, board_height)
        .translate((0, 0, z_pos))
    )
    
    # Apply chamfer to top edges to simulate V-groove between boards
    # Select edges that are parallel to X and near the top of this specific board
    # Top face Z coordinate is z_pos + board_height/2
    top_z = z_pos + board_height/2
    current_board = current_board.edges(
        cq.selectors.BoxSelector(
            (-board_length, -board_thickness, top_z - 1),
            (board_length, board_thickness, top_z + 1)
        )
    ).chamfer(5.0)

    boards = boards.union(current_board)


# 4. Top Cap (Handrail)
# The image shows a top rail that covers the boards and the tops of the posts slightly?
# No, actually the posts stick up past the boards. There is a top board that looks slightly different or just the top of the stack.
# There looks to be a thinner capping rail on top of the boards, running between posts.
cap_width = board_thickness + 20.0
cap_height = 30.0
cap_rail = (
    cq.Workplane("XY")
    .box(board_length, cap_width, cap_height)
    .translate((0, 0, panel_height + cap_height/2))
)
# The image doesn't clearly show a separate cap rail distinct from the top board, 
# but often these fences have a U-channel or a cap.
# Looking closely at the top right, the top board seems to have a flat top, unlike the others.
# Let's assume the top board is the cap rail.

# Let's combine components.
# The boards penetrate the posts.
# To make it look manufactured, we should cut the slot in the posts.

slot_cutout = (
    cq.Workplane("XY")
    .box(panel_width, board_thickness + 2.0, panel_height) # Slightly wider for tolerance
    .translate((0, 0, panel_height/2))
)

left_post_slotted = left_post.cut(slot_cutout)
right_post_slotted = right_post.cut(slot_cutout)

# Combine everything
result = left_post_slotted.union(right_post_slotted).union(boards)

# If there is a specific top cap shown in the image (it's a bit ambiguous, 
# looks like a board on top), let's add a simple cover strip.
top_cover = (
    cq.Workplane("XY")
    .box(board_length, board_thickness + 10, 15) # Slightly wider than boards
    .translate((0, 0, panel_height + 15/2))
)

# Merge the top cover if deemed part of the design. 
# Looking at the image, the top edge is clean. Let's add it.
result = result.union(top_cover)

# Final adjustment: Move to positive Z
# The current model starts at Z=0 and goes up.

# Export or Render
if 'show_object' in globals():
    show_object(result)