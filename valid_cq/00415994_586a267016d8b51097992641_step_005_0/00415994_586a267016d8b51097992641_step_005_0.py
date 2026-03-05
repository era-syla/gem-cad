import cadquery as cq

# ==========================================
# Parameters & Dimensions
# ==========================================

# Overall layout
total_length = 180.0
nose_ratio = 0.35
nose_length = total_length * nose_ratio
body_length = total_length * (1 - nose_ratio)

# Widths
nose_width = 35.0
body_width = 60.0  # The main body is wider than the nose

# Heights
base_height = 25.0  # Height of the nose block and the body deck
wall_height_rear = 65.0  # Maximum height of the side walls at the rear

# Material thickness
wall_th = 4.0

# ==========================================
# 1. Nose Section (Front)
# ==========================================
# Create the base block for the nose
nose = cq.Workplane("XY").box(nose_length, nose_width, base_height)\
    .translate((nose_length/2, 0, base_height/2))

# Add T-Slot Feature on top
# Longitudinal cut
nose = nose.faces(">Z").workplane().center(-5, 0)\
    .rect(25, 8).cutBlind(-5)
# Transverse cut (forming the T)
nose = nose.faces(">Z").workplane().center(-15, 0)\
    .rect(10, 22).cutBlind(-5)

# Add Bolt Holes
nose = nose.faces(">Z").workplane().pushPoints([
    (20, 10), (20, -10), 
    (-22, 10), (-22, -10)
]).circle(2.5).cutBlind(-base_height)

# ==========================================
# 2. Body Deck (Middle)
# ==========================================
# Create the floor of the main body
body_deck = cq.Workplane("XY").box(body_length, body_width, base_height)\
    .translate((nose_length + body_length/2, 0, base_height/2))

# Add Grid of Holes
# Generate a pattern of points
holes_pts = []
rows = 3
cols = 6
x_start = -body_length/2 + 12
y_start = -body_width/2 + 12
x_step = 14
y_step = 18

for c in range(cols):
    for r in range(rows):
        holes_pts.append((x_start + c*x_step, y_start + r*y_step))

body_deck = body_deck.faces(">Z").workplane().pushPoints(holes_pts)\
    .circle(1.8).cutBlind(-base_height)

# ==========================================
# 3. Side Walls with Curved Profile
# ==========================================
def create_side_wall(y_offset):
    """
    Creates a side wall profile on the XZ plane and extrudes it.
    The profile creates the 'swooping' look.
    """
    # Define key points
    pt_front_top = (nose_length, base_height)
    pt_front_bot = (nose_length, 0)
    pt_back_bot = (total_length, 0)
    pt_back_top = (total_length, wall_height_rear)
    
    # Control point for the arc to create a concave ramp
    pt_mid_arc = (nose_length + body_length * 0.4, base_height + 8)
    
    # Draw profile on XZ plane at specific Y offset
    wall = cq.Workplane("XZ").workplane(offset=y_offset)\
        .moveTo(*pt_front_bot)\
        .lineTo(*pt_back_bot)\
        .lineTo(*pt_back_top)\
        .threePointArc(pt_mid_arc, pt_front_top)\
        .close()\
        .extrude(wall_th)
    return wall

# Right Wall (Positive Y)
# Offset so the inner face aligns with body_width/2
wall_right = create_side_wall(body_width/2)

# Left Wall (Negative Y)
# Offset so the inner face aligns with -body_width/2
# Extrude goes in positive Y normal direction, so we start at -(width/2 + thickness)
wall_left = create_side_wall(-body_width/2 - wall_th)

# ==========================================
# 4. Rear Bulkhead & Details
# ==========================================
# Vertical plate at the very back
rear_blk = cq.Workplane("XY").box(wall_th, body_width + 2*wall_th, wall_height_rear)\
    .translate((total_length - wall_th/2, 0, wall_height_rear/2))

# Large circular cutout
rear_blk = rear_blk.faces(">X").workplane().center(0, 15)\
    .circle(14).cutBlind(-wall_th)

# Rectangular detail cutout
rear_blk = rear_blk.faces(">X").workplane().center(18, -10)\
    .rect(8, 15).cutBlind(-wall_th)

# ==========================================
# 5. Middle Tab Feature
# ==========================================
# Small vertical bracket in the middle of the deck
tab_pos_x = nose_length + body_length * 0.45
tab = cq.Workplane("XY").box(2, 20, 25)\
    .translate((tab_pos_x, 0, base_height + 12.5))

# Hole in the tab
tab = tab.faces(">X").workplane().circle(5).cutBlind(-2)

# ==========================================
# 6. Assembly
# ==========================================
# Combine all solid parts into one result
result = nose.union(body_deck)\
             .union(wall_right)\
             .union(wall_left)\
             .union(rear_blk)\
             .union(tab)