import cadquery as cq

# --- Parameters ---

# Main Housing Body
housing_length = 50
housing_width = 30
housing_thickness = 12
housing_fillet = 2.0
nozzle_diam = 6
nozzle_length = 8
nozzle_hole = 3.5

# Gripper Arms (Claws)
claw_length = 40
claw_thickness = 5
claw_base_width = 12
claw_tip_width = 4
num_teeth = 5
tooth_depth = 2.5
claw_hole_diam = 3.2

# Linkage Bars
link_length = 15
link_width = 6
link_thickness = 2.5
link_hole_diam = 2.5

# Sliding Block
block_length = 12
block_width = 10
block_height = 8
block_hole_diam = 3.0

# Pivot Pins (represented as simple cylinders in the exploded view)
pin_diam_large = 4.0
pin_head_diam = 6.0
pin_length_large = 14
pin_diam_small = 2.5
pin_length_small = 8

# --- Helper Functions ---

def create_claw_profile(length, base_w, tip_w, teeth, t_depth):
    """Creates a 2D profile of a serrated claw."""
    # Define points for the outer curve
    pts = [
        (0, 0),
        (length, base_w/2 - tip_w), # Tip point inner
        (length, base_w/2), # Tip point outer
        (0, base_w)  # Base top
    ]
    
    # Outer spline
    path = cq.Workplane("XY").moveTo(0, 0).lineTo(length, -tip_w).lineTo(length, 0)
    
    # Inner serrated edge logic
    # We will draw the rough shape then cut the teeth or build the teeth
    # Let's try drawing the profile directly
    
    x_step = length / (teeth + 1)
    
    s = cq.Workplane("XY").moveTo(0, 0)
    
    # Draw the inner edge with teeth
    current_x = 0
    current_y = 0
    
    # Base area
    s = s.lineTo(5, 0)
    current_x = 5
    
    remaining_len = length - 5
    tooth_span = remaining_len / teeth
    
    for i in range(teeth):
        # Tooth valley
        s = s.lineTo(current_x + tooth_span/2, current_y + t_depth)
        # Tooth peak
        s = s.lineTo(current_x + tooth_span, current_y)
        current_x += tooth_span
        
    # Curved outer back
    # Using a 3-point arc approximation or Spline
    s = s.lineTo(length, 8) # Tip thickness
    s = s.threePointArc((length/2, 12), (0, 10))
    s = s.close()
    
    return s

# --- Part Construction ---

# 1. Main Housing
# Create a chamfered rectangular body
housing_base = (
    cq.Workplane("XY")
    .rect(housing_length, housing_width)
    .extrude(housing_thickness)
    .edges("|Z").fillet(housing_fillet)
)

# Cut the interior slot for the sliding mechanism
housing = (
    housing_base
    .faces(">Z").workplane()
    .rect(housing_length + 2, housing_width - 8) # Through slot
    .cutBlind(-housing_thickness + 2) # Leave a floor
)

# Add the nozzle/tube connector at the back
nozzle = (
    cq.Workplane("YZ")
    .circle(nozzle_diam/2)
    .extrude(nozzle_length)
    .translate((-housing_length/2 - nozzle_length, 0, housing_thickness/2))
)

# Nozzle Hole
nozzle_hole_cut = (
    cq.Workplane("YZ")
    .circle(nozzle_hole/2)
    .extrude(nozzle_length + 5)
    .translate((-housing_length/2 - nozzle_length, 0, housing_thickness/2))
)

# Add pivot holes for claws
pivot_hole_locs = [(housing_length/2 - 5, housing_width/2 - 4), 
                   (housing_length/2 - 5, -housing_width/2 + 4)]

housing = (
    housing
    .union(nozzle)
    .cut(nozzle_hole_cut)
    .faces(">Z").workplane()
    .pushPoints(pivot_hole_locs)
    .hole(pin_diam_large)
)

# Cut front opening for claws
housing = (
    housing
    .faces(">X").workplane()
    .rect(10, housing_width - 4)
    .cutBlind(-15)
)


# 2. Sliding Actuating Block
block = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height)
    .faces(">X").workplane()
    .hole(block_hole_diam, depth=5) # Connection hole
)

# Add pivot ears to block for linkages
block_ears = (
    cq.Workplane("XY")
    .rect(4, block_width + 4)
    .extrude(block_height)
    .translate((block_length/2 - 2, 0, 0))
)
# Drill holes in ears
block = block.union(block_ears)
block = (
    block
    .faces(">Z").workplane()
    .pushPoints([(block_length/2 - 2, block_width/2 + 1), (block_length/2 - 2, -(block_width/2 + 1))])
    .hole(2.0)
)
# Center the block relative to origin for assembly view
block = block.translate((-housing_length/2 - 15, 0, 2))


# 3. Gripper Arms (Claws)
# Define a custom shape for the claw
def make_claw(direction=1):
    pts = [
        (0,0), (5,0), (10, -2), (15, 0), (20, -2), (25, 0), (30, -2), (35, 0), # Teeth
        (38, 2), # Tip
        (35, 6), (20, 10), (5, 8), (0, 8) # Back curve
    ]
    
    claw_outline = (
        cq.Workplane("XY")
        .polyline(pts).close()
        .extrude(claw_thickness)
    )
    
    # Add pivot hinge at base
    hinge = (
        cq.Workplane("XY")
        .circle(4)
        .extrude(claw_thickness)
        .translate((0, 4, 0))
    )
    
    # Add linkage connection point
    link_conn = (
        cq.Workplane("XY")
        .circle(3)
        .extrude(claw_thickness)
        .translate((5, 10, 0)) # Offset position
    )
    
    full_claw = claw_outline.union(hinge).union(link_conn)
    
    # Holes
    full_claw = (
        full_claw
        .faces(">Z").workplane()
        .pushPoints([(0, 4), (5, 10)])
        .hole(claw_hole_diam)
    )
    
    if direction == -1:
        full_claw = full_claw.mirror("XZ")
        
    return full_claw

claw_left = make_claw(1).translate((housing_length/2 + 10, housing_width/2 + 5, housing_thickness/2 - claw_thickness/2))
claw_right = make_claw(-1).translate((housing_length/2 + 10, -housing_width/2 - 5, housing_thickness/2 - claw_thickness/2))


# 4. Linkage Bars
# Simple dog-bone shape
linkage = (
    cq.Workplane("XY")
    .circle(link_width/2)
    .extrude(link_thickness)
    .translate((-link_length/2, 0, 0))
    .union(
        cq.Workplane("XY")
        .circle(link_width/2)
        .extrude(link_thickness)
        .translate((link_length/2, 0, 0))
    )
    .union(
        cq.Workplane("XY")
        .rect(link_length, link_width)
        .extrude(link_thickness)
    )
)
# Holes
linkage = (
    linkage
    .faces(">Z").workplane()
    .pushPoints([(-link_length/2, 0), (link_length/2, 0)])
    .hole(link_hole_diam)
)

link_1 = linkage.translate((0, -20, 0))
link_2 = linkage.translate((0, -30, 0))


# 5. Pins (Exploded view decoration)
pin_large = (
    cq.Workplane("XY")
    .circle(pin_head_diam/2).extrude(2)
    .faces("<Z").workplane()
    .circle(pin_diam_large/2).extrude(pin_length_large)
    .translate((-10, 25, 0)) # Random placement for exploded view
)

pin_small = (
    cq.Workplane("XY")
    .circle(pin_diam_small/2).extrude(pin_length_small)
    .translate((-5, -25, 0))
)

# --- Assembly / Layout ---
# Combine all parts into one result for the exploded view similar to image

result = (
    housing
    .union(block)
    .union(claw_left)
    .union(claw_right)
    .union(link_1)
    .union(link_2)
    .union(pin_large)
    .union(pin_small)
)