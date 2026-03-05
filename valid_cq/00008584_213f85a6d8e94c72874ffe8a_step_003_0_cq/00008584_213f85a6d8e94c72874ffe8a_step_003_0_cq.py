import cadquery as cq

# --- Parametric Variables ---
# Profile Dimensions (assuming standard aluminum extrusion or square tube)
profile_w = 20.0  # Width of the square profile
profile_h = 20.0  # Height of the square profile
wall_thickness = 2.0  # Wall thickness for the tube

# Structure Dimensions
vertical_post_height = 800.0
horizontal_arm_length = 1200.0
secondary_vertical_length = 400.0
short_vertical_offset_x = 200.0 # Distance from main post to floating vertical bar

# Hardware/Joint Details
joint_plate_size = 40.0
joint_plate_thick = 4.0
bolt_head_dia = 10.0
bolt_head_thick = 5.0
foot_dia = 50.0
foot_thick = 5.0
slider_block_size = 30.0

# --- Helper Functions ---

def create_tube(length, w, h, t):
    """Creates a hollow square tube."""
    outer = cq.Workplane("XY").box(length, w, h)
    inner = cq.Workplane("XY").box(length, w - 2*t, h - 2*t)
    return outer.cut(inner)

def create_joint_bracket():
    """Creates a simple L-bracket or joining plate visual representation."""
    return cq.Workplane("XY").box(joint_plate_size, joint_plate_thick, joint_plate_size)

def create_foot():
    """Creates a circular foot base."""
    return cq.Workplane("XY").circle(foot_dia/2).extrude(foot_thick)

def create_knob_screw():
    """Creates a simple knob/bolt representation."""
    shank = cq.Workplane("XY").circle(3).extrude(30)
    head = cq.Workplane("XY").circle(bolt_head_dia/2).extrude(bolt_head_thick).translate((0,0,30))
    return shank.union(head)

# --- Component Construction ---

# 1. Main Vertical Post
# Oriented along Z axis
main_post = create_tube(vertical_post_height, profile_w, profile_h, wall_thickness)
main_post = main_post.rotate((0,1,0), (0,0,0), 90) # Rotate box to stand up
main_post = main_post.translate((0, 0, vertical_post_height/2))

# 2. Main Horizontal Arm
# Oriented along X axis, attached to the top of the main post
horizontal_arm = create_tube(horizontal_arm_length, profile_w, profile_h, wall_thickness)
horizontal_arm = horizontal_arm.translate((horizontal_arm_length/2 + profile_w/2, 0, vertical_post_height - profile_h/2))

# 3. Corner Joint (Top Left)
# Visual representation of a bracket connecting the two
corner_bracket = create_joint_bracket()
corner_bracket = corner_bracket.translate((profile_w/2 + joint_plate_thick/2, 0, vertical_post_height - joint_plate_size/2))

# 4. Floating Vertical Bar (The one hanging down slightly offset)
# It appears to be separate or waiting for assembly in the image
floating_bar = create_tube(secondary_vertical_length, profile_w, profile_h, wall_thickness)
floating_bar = floating_bar.rotate((0,1,0), (0,0,0), 90)
floating_bar = floating_bar.translate((short_vertical_offset_x, 0, vertical_post_height/2)) # Position roughly in middle for visual

# 5. Base/Foot details
# Circular foot at the bottom of the main post
base_foot = create_foot()
base_foot = base_foot.translate((0, 0, -foot_thick))

# Small rectangular blocks near the base (possibly weights or mounts)
base_block_1 = cq.Workplane("XY").box(40, 20, 25).translate((40, 0, 12.5))
base_block_2 = cq.Workplane("XY").box(40, 20, 25).translate((85, 0, 12.5))

# 6. Slider/Adjustment Mechanism on Main Post
# A block that slides on the vertical post with a knob
slider_block = cq.Workplane("XY").box(profile_w + 10, profile_w + 10, slider_block_size)
slider_cutout = cq.Workplane("XY").box(profile_w, profile_w, slider_block_size)
slider = slider_block.cut(slider_cutout)
slider = slider.translate((0, 0, vertical_post_height * 0.4)) # Positioned partway up

# Knob on the slider
slider_knob = create_knob_screw()
slider_knob = slider_knob.rotate((1,0,0), (0,0,0), -90)
slider_knob = slider_knob.translate((0, -(profile_w/2 + 5), vertical_post_height * 0.4))

# 7. Vertical Pin/Stop on the Horizontal Arm
# A pin sticking up from the long horizontal arm
pin_loc_x = horizontal_arm_length * 0.7
vertical_pin = cq.Workplane("XY").circle(3).extrude(100)
vertical_pin = vertical_pin.translate((pin_loc_x, 0, vertical_post_height))

# Mounting block for the pin
pin_block = cq.Workplane("XY").box(20, 25, 20)
pin_block = pin_block.translate((pin_loc_x, 0, vertical_post_height + 10))


# --- Assembly ---

result = (
    main_post
    .union(horizontal_arm)
    .union(corner_bracket)
    .union(floating_bar)
    .union(base_foot)
    .union(base_block_1)
    .union(base_block_2)
    .union(slider)
    .union(slider_knob)
    .union(vertical_pin)
    .union(pin_block)
)