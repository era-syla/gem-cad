import cadquery as cq

# -----------------------------------------------------------------------------
# Parametric Dimensions
# -----------------------------------------------------------------------------

# Plate Parameters
plate_width = 30.0
plate_height = 30.0
plate_thickness = 3.0
plate_fillet = 1.0

# Hole Parameters
hole_dia = 3.2  # Clearance for M3
hole_spacing_x = 18.0
hole_spacing_y = 12.0  # From center, or spacing between them? Let's assume symmetric about Y
hole_offset_top = 8.0 # From top edge to hole center

# Neck/Joint Connection Parameters
neck_width = 8.0
neck_thickness = 4.0
neck_length = 8.0
neck_fillet = 1.0

# Ball Parameters (Male Part)
ball_dia = 10.0
ball_neck_dia = 5.0
ball_neck_length = 5.0

# Socket Parameters (Female Part)
socket_outer_dia = 13.0
socket_inner_dia = 10.2 # Slight clearance for the 10mm ball
socket_height = 12.0
socket_wall_thickness = 1.5
socket_cut_width = 3.0 # Width of the slots in the socket

# Distance between the two parts for visualization
part_spacing = 50.0

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def create_base_plate():
    """Creates the standard mounting plate with holes."""
    plate = (
        cq.Workplane("XY")
        .box(plate_width, plate_height, plate_thickness)
        .edges("|Z")
        .fillet(plate_fillet)
    )
    
    # Create counterbored holes
    # Assuming holes are centered horizontally and offset from top
    # Let's arrange them like the left image (2 holes) vs right image (4 holes).
    # The image actually shows the BACK of the left part (2 large holes) and FRONT of right part (4 small holes).
    # Wait, looking closer:
    # Left part: 2 holes, horizontally aligned.
    # Right part: 4 small holes near corners.
    # To keep it simple and parametric, I'll generate the Left style plate for the Socket 
    # and the Right style plate for the Ball, as per the image.
    
    return plate

# -----------------------------------------------------------------------------
# Part 1: The Socket Part (Left in image)
# -----------------------------------------------------------------------------

# Base Plate
socket_plate = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .edges("|Z").fillet(plate_fillet)
)

# Holes for Socket Plate (2 large holes)
socket_plate = (
    socket_plate
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing_x/2, 0), (hole_spacing_x/2, 0)])
    .cskHole(hole_dia, hole_dia * 2, 82) # Countersunk
)

# Connection Neck
# The neck connects the bottom edge of the plate to the socket cup
neck_pos_y = -plate_height/2 - neck_length/2
socket_neck = (
    cq.Workplane("XY")
    .workplane(offset=-plate_thickness/2) # Align with back face or center? Let's center.
    .center(0, -plate_height/2)
    .box(neck_width, neck_length * 2, plate_thickness) # Overlap to merge
    .edges("|Z").fillet(neck_fillet)
)

# The Socket Cup
socket_center = (0, -plate_height/2 - neck_length, 0)

socket_cup = (
    cq.Workplane("XY")
    .workplane(offset=-socket_height/2) # Start drawing from bottom? No, simpler to revolve or sphere.
    .center(*socket_center[:2])
    .sphere(socket_outer_dia/2)
)

# Cut the inner sphere for the socket
socket_cup = socket_cup.cut(
    cq.Workplane("XY")
    .center(*socket_center[:2])
    .sphere(socket_inner_dia/2)
)

# Cut the bottom flat
socket_cup = socket_cup.cut(
    cq.Workplane("XY")
    .center(*socket_center[:2])
    .workplane(offset=-socket_outer_dia)
    .box(socket_outer_dia*2, socket_outer_dia*2, socket_outer_dia)
)

# Cut the slots to allow expansion
# We need an X-shaped cut or 4 slots.
slot_cutter = (
    cq.Workplane("XY")
    .center(*socket_center[:2])
    .rect(socket_cut_width, socket_outer_dia * 2)
    .extrude(socket_outer_dia * 2, both=True)
)
slot_cutter_2 = slot_cutter.rotate((0,0,0), (0,0,1), 90)

socket_cup = socket_cup.cut(slot_cutter).cut(slot_cutter_2)

# Join Socket parts
part1 = socket_plate.union(socket_neck).union(socket_cup)

# Add fillets to the neck-cup junction for strength
# This is tricky with boolean unions, approximate with a small fillet on the neck edge if possible,
# or just leave as joined solids.

# -----------------------------------------------------------------------------
# Part 2: The Ball Part (Right in image)
# -----------------------------------------------------------------------------

# Base Plate
ball_plate = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .edges("|Z").fillet(plate_fillet)
)

# Holes for Ball Plate (4 small holes near corners)
# Based on image, corner spacing
corner_spacing = 5.0
holes_x = plate_width/2 - corner_spacing
holes_y = plate_height/2 - corner_spacing

ball_plate = (
    ball_plate
    .faces(">Z")
    .workplane()
    .rect(holes_x * 2, holes_y * 2, forConstruction=True)
    .vertices()
    .hole(2.0) # Smaller screw holes
)

# Center rectangular cutout (as seen in image)
ball_plate = (
    ball_plate
    .faces(">Z")
    .workplane()
    .rect(10, 10)
    .cutBlind(-plate_thickness)
)

# Connection Neck
# Connects bottom of plate to ball.
# It seems to have a transition.
ball_neck = (
    cq.Workplane("XY")
    .center(0, -plate_height/2)
    .box(neck_width, neck_length * 2, plate_thickness) # Overlap
    .edges("|Z").fillet(neck_fillet)
)

# The Ball
ball_center_y = -plate_height/2 - neck_length - ball_dia/2 + 2 # Adjust position
ball_obj = (
    cq.Workplane("XY")
    .center(0, ball_center_y)
    .sphere(ball_dia/2)
)

# Stem connecting neck to ball (cylinder)
stem = (
    cq.Workplane("YZ")
    .center(0, ball_center_y + ball_dia/2) # Start at ball center roughly
    .workplane(offset=0) 
    # We need a cylinder pointing up towards the plate
    # Rotate workplane to lay cylinder along Y axis
)

stem = (
    cq.Workplane("XZ") # Front plane
    .workplane(offset=ball_center_y) # Move to ball center
    .circle(ball_neck_dia/2)
    .extrude(ball_neck_length + 5) # Extrude towards plate
)

# Join Ball parts
part2 = ball_plate.union(ball_neck).union(ball_obj).union(stem)


# -----------------------------------------------------------------------------
# Final Assembly / Positioning
# -----------------------------------------------------------------------------

# Rotate parts to stand upright as in the image (Image is roughly isometric view of upright plates)
# The current Z is thickness. Let's rotate -90 around X to make them stand up.

part1_upright = part1.rotate((0,0,0), (1,0,0), -90) # Socket part (Left)
part2_upright = part2.rotate((0,0,0), (1,0,0), -90).translate((part_spacing, 0, 0)) # Ball part (Right)

result = part1_upright.union(part2_upright)