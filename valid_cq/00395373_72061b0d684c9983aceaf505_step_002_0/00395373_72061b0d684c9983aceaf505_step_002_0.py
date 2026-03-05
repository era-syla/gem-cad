import cadquery as cq

# --- Parameters ---
# Torso dimensions
torso_length = 65.0
torso_width = 38.0
torso_thick = 22.0
fillet_radius = 8.0

# Head dimensions
neck_len = 8.0
neck_rad = 7.0
head_len = 24.0
head_rad = 11.5

# Leg dimensions
leg_len = 85.0
leg_rad = 9.0
leg_spacing = 11.0 # Offset from center Y
foot_len = 18.0
foot_height = 25.0

# Arm dimensions
shoulder_rad = 9.5
upper_arm_len = 38.0
upper_arm_rad = 7.5
forearm_len = 32.0
forearm_rad = 6.5
hand_size = 10.0

# --- Geometry Construction ---

# 1. Torso
# Create a central body block with rounded edges to resemble a chest/abdomen
torso = (cq.Workplane("XY")
         .box(torso_length, torso_width, torso_thick)
         .edges("|X")
         .fillet(fillet_radius)
         .edges("|Y")
         .fillet(3.0))

# 2. Head & Neck
# Neck cylinder
neck_pos_x = torso_length / 2
neck = (cq.Workplane("YZ")
        .workplane(offset=neck_pos_x)
        .circle(neck_rad)
        .extrude(neck_len))

# Head cylinder and dome
head_pos_x = neck_pos_x + neck_len
head_main = (cq.Workplane("YZ")
             .workplane(offset=head_pos_x)
             .circle(head_rad)
             .extrude(head_len))

head_top = (cq.Workplane("YZ")
            .workplane(offset=head_pos_x + head_len)
            .sphere(head_rad))

# 3. Legs and Feet
def create_leg(y_offset):
    # Main leg cylinder (extruding backwards in X)
    # Start slightly inside the torso for connection
    start_x = -torso_length / 2 + 5
    leg_cyl = (cq.Workplane("YZ")
               .workplane(offset=start_x)
               .center(y_offset, 0)
               .circle(leg_rad)
               .extrude(-(leg_len + 5)))
    
    # Foot location
    foot_x = start_x - (leg_len + 5)
    
    # Foot shape: A block sticking up +Z
    foot = (cq.Workplane("XY")
            .center(foot_x - foot_len/2 + leg_rad, y_offset)
            .box(foot_len, leg_rad*2, foot_height)
            .edges("|Y").fillet(2.0)
            .translate((0, 0, foot_height/2 - leg_rad))) # Shift up to align bottom
            
    return leg_cyl.union(foot)

left_leg = create_leg(leg_spacing)
right_leg = create_leg(-leg_spacing)

# 4. Arms (Shoulders, Upper Arm, Forearm, Hand)
def create_arm(is_left):
    side_sign = 1 if is_left else -1
    y_pos = side_sign * (torso_width/2 + 2)
    shoulder_x = torso_length/2 - 12
    
    # Shoulder Sphere
    shoulder = (cq.Workplane("XY")
                .center(shoulder_x, y_pos)
                .sphere(shoulder_rad))
    
    # Upper Arm: Extrude -X from shoulder plane
    upper_arm = (cq.Workplane("YZ")
                 .workplane(offset=shoulder_x)
                 .center(y_pos, 0)
                 .circle(upper_arm_rad)
                 .extrude(-upper_arm_len))
    
    # Elbow Sphere
    elbow_x = shoulder_x - upper_arm_len
    elbow = (cq.Workplane("XY")
             .center(elbow_x, y_pos)
             .sphere(upper_arm_rad))
    
    # Forearm: Extrude +Z (Upwards)
    forearm = (cq.Workplane("XY")
               .center(elbow_x, y_pos)
               .circle(forearm_rad)
               .extrude(forearm_len))
    
    # Hand: Simple pincer/clip shape at top
    hand = (cq.Workplane("XY")
            .center(elbow_x, y_pos)
            .workplane(offset=forearm_len)
            .box(8, 12, 12)
            .edges().fillet(1.0))
            
    return shoulder.union(upper_arm).union(elbow).union(forearm).union(hand)

left_arm = create_arm(True)
right_arm = create_arm(False)

# --- Assembly ---
result = (torso
          .union(neck)
          .union(head_main)
          .union(head_top)
          .union(left_leg)
          .union(right_leg)
          .union(left_arm)
          .union(right_arm))

# Optional: Add a subtle centerline groove to match the dummy style
groove = cq.Workplane("XY").box(torso_length*0.8, 1.5, torso_thick + 2)
result = result.cut(groove)