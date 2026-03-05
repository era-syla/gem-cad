import cadquery as cq

# --- Parametric Dimensions ---
frame_length = 2200.0
frame_width = 1300.0
tube_size = 35.0  # Square tubing profile size
leg_height = 180.0
leg_width = 40.0  # Width of the leg strap
leg_thick = 6.0   # Thickness of the leg strap
hook_reach = 60.0 # How far the leg hooks inwards
num_crossbars = 4

# --- Helper Functions ---

def create_leg_pair(y_position, rail_offset, z_start):
    """Creates a pair of legs at a specific Y position."""
    
    legs = cq.Workplane("XY")
    
    # Right Leg (Hook/Gutter Style) - Located at +X
    # 1. Vertical segment descending from rail
    r_vert = cq.Workplane("XY").box(leg_thick, leg_width, leg_height)\
        .translate((rail_offset, y_position, z_start - leg_height/2))
    
    # 2. Horizontal segment hooking inwards (-X)
    h_x_pos = rail_offset - hook_reach/2
    h_z_pos = z_start - leg_height + leg_thick/2
    r_horz = cq.Workplane("XY").box(hook_reach, leg_width, leg_thick)\
        .translate((h_x_pos, y_position, h_z_pos))
        
    # 3. Small vertical tip descending from hook
    tip_len = 25.0
    t_x_pos = rail_offset - hook_reach + leg_thick/2
    t_z_pos = h_z_pos - tip_len/2 - leg_thick/2
    r_tip = cq.Workplane("XY").box(leg_thick, leg_width, tip_len)\
        .translate((t_x_pos, y_position, t_z_pos))
        
    # 4. Foot pad
    r_pad = cq.Workplane("XY").box(30, 50, 5)\
        .translate((t_x_pos, y_position, t_z_pos - tip_len/2 - 2.5))
        
    legs = legs.union(r_vert).union(r_horz).union(r_tip).union(r_pad)
    
    # Left Leg (Straight/Post Style) - Located at -X
    # Based on image, left legs appear straight
    l_vert = cq.Workplane("XY").box(leg_thick, leg_width, leg_height)\
        .translate((-rail_offset, y_position, z_start - leg_height/2))
        
    l_pad = cq.Workplane("XY").box(40, 50, 5)\
        .translate((-rail_offset, y_position, z_start - leg_height - 2.5))
        
    legs = legs.union(l_vert).union(l_pad)
    
    return legs

# --- Main Construction ---

# 1. Create Side Rails
# Offset from center
rail_x_offset = (frame_width - tube_size) / 2.0

left_rail = cq.Workplane("XY").box(tube_size, frame_length, tube_size)\
    .translate((-rail_x_offset, 0, 0))

right_rail = cq.Workplane("XY").box(tube_size, frame_length, tube_size)\
    .translate((rail_x_offset, 0, 0))

frame = left_rail.union(right_rail)

# 2. Create Crossbars
# Calculate positions for evenly spaced bars
# We assume bars are flush with the ends of the rails
start_y = -(frame_length - tube_size) / 2.0
step_y = (frame_length - tube_size) / (num_crossbars - 1)
bar_length = frame_width - 2 * tube_size # Fits between rails

crossbar_positions = []

for i in range(num_crossbars):
    y_pos = start_y + i * step_y
    crossbar_positions.append(y_pos)
    
    bar = cq.Workplane("XY").box(bar_length, tube_size, tube_size)\
        .translate((0, y_pos, 0))
    frame = frame.union(bar)

# 3. Add Legs
# Based on image analysis, legs are at specific crossbar indices (0, 1, 3)
# 0 = Front, 1 = Middle-Front, 3 = Back (skipping index 2)
leg_indices = [0, 1, 3]
z_attachment = -tube_size / 2.0

all_legs = cq.Workplane("XY")

for idx in leg_indices:
    y_loc = crossbar_positions[idx]
    leg_pair = create_leg_pair(y_loc, rail_x_offset, z_attachment)
    all_legs = all_legs.union(leg_pair)

# Final Boolean Union
result = frame.union(all_legs)