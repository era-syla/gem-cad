import cadquery as cq

# Parametric dimensions
width = 100.0       # Total width of the frame
height = 80.0       # Total height of the frame
thickness = 5.0     # Thickness of the plate
frame_width = 10.0  # Width of the frame border (top and sides)
bottom_height = 15.0 # Height of the bottom section (looks slightly taller than sides)
foot_height = 5.0   # How much the legs extend down past the bottom rail (if any), 
                    # but looking at the image, it's just a rectangular hole.
                    # Let's reinterpret: It's a rectangular plate with a rectangular cutout.
                    # The cutout is offset from the bottom edge more than the other edges?
                    # Or maybe it has "feet". Let's look at the bottom corners.
                    # The bottom corners extend downwards. It looks like an inverted "U" shape combined with a bottom crossbar,
                    # or a rectangular frame where the bottom rail is raised up, creating two "feet".

# Refined Geometry Strategy:
# 1. Create a main rectangle (the outer boundary).
# 2. Create a cutout rectangle (the inner window).
# 3. Create a cutout at the bottom to form the "feet".

# Dimensions based on estimation from the isometric view:
total_width = 100.0
total_height = 80.0
depth = 5.0

# Frame border thickness
side_border = 10.0
top_border = 10.0
bottom_rail_height = 15.0 # The horizontal bar at the bottom
leg_height = 10.0         # The small vertical extensions at the bottom corners

# Calculating the inner window dimensions
window_width = total_width - (2 * side_border)
# The window starts after the bottom rail and ends before the top border.
# However, the "legs" imply a cutout at the very bottom center.

# Let's try a constructive approach:
# 1. Draw the outer profile.
# 2. Draw the inner profile (the window).
# 3. Extrude.

# Let's define the 2D sketch on the XY plane.
# Outer shape is a rectangle of total_width x total_height.
# Inner shape is a rectangle for the window.
# Bottom shape is a cutout between the legs.

# Re-evaluating the image:
# It looks like a standard rectangular frame, but the bottom edge has a rectangular cutout in the middle, leaving two "feet".
# Or, simply, the bottom rail is higher up than the bottom of the side legs.

# Parameters
W = 120.0  # Total Width
H = 90.0   # Total Height
T = 5.0    # Thickness
border_w = 15.0 # Side border width
top_w = 15.0    # Top border width
bottom_rail_h = 20.0 # Height of the bottom horizontal bar
leg_h = 10.0   # Height of the legs (distance from bottom of rail to floor)

# Derived dimensions for the window
window_w = W - 2 * border_w
window_h = H - top_w - bottom_rail_h - leg_h 
# Wait, looking at the image, the window is enclosed. 
# It's a closed loop frame.
# And then there is a notch at the bottom.

# Let's construct it as a sketch.
# Center the object roughly.

result = (
    cq.Workplane("XY")
    .rect(W, H) # Base rectangle
    .extrude(T)
    # Cut the main window
    .faces(">Z")
    .workplane()
    .rect(W - 2*border_w, H - top_w - (bottom_rail_h + leg_h)) 
    # Positioning the window: 
    # Vertical center of window needs to be calculated.
    # The solid part at top is top_w.
    # The solid part at bottom is (bottom_rail_h + leg_h).
    # Shift Y = ( (bottom_rail_h + leg_h) - top_w ) / 2
    .center(0, ((bottom_rail_h + leg_h) - top_w) / 2)
    .cutBlind(-T)
    # Cut the space between the legs at the bottom
    .faces(">Z")
    .workplane()
    # Reset origin to center of top face
    .center(0, -H/2 + leg_h/2) 
    .rect(W - 2*border_w, leg_h)
    .cutBlind(-T)
)

# Actually, a cleaner way is just drawing the 2D profile and extruding.
# Let's trace the "wire" of the face.

def create_frame():
    # Dimensions
    width = 100.0
    height = 80.0
    thickness = 5.0
    
    side_frame_width = 12.0
    top_frame_width = 12.0
    bottom_rail_height = 15.0
    leg_height = 8.0 # The gap at the bottom

    # Outer points
    # (0,0) is bottom-left of the left leg
    pts = [
        (0, 0),
        (width, 0),
        (width, height),
        (0, height),
        (0, 0) # close outer loop
    ]
    
    # Inner Window
    # The window starts above the (leg_height + bottom_rail_height)
    # And ends top_frame_width from top.
    
    window_x1 = side_frame_width
    window_x2 = width - side_frame_width
    window_y1 = leg_height + bottom_rail_height
    window_y2 = height - top_frame_width
    
    # Bottom Notch (between legs)
    # Starts at x=side_frame_width, ends x=width-side_frame_width
    # Height is from 0 to leg_height
    
    # It is easier to subtract rectangles from a main plate.
    
    base = cq.Workplane("XY").box(width, height, thickness)
    
    # Cut the window
    # Window center relative to box center (0,0,0)
    # Box goes from -width/2 to width/2, -height/2 to height/2
    
    # Window geometry in global coords (assuming bottom-left is 0,0 for thinking):
    # W_center_x = width/2
    # W_center_y = window_y1 + (window_y2 - window_y1)/2
    
    # Shift to box local coords:
    w_center_y_local = (window_y1 + (window_y2 - window_y1)/2) - height/2
    w_height = window_y2 - window_y1
    w_width = window_x2 - window_x1
    
    base = base.faces(">Y").workplane().center(0, 0).rect(w_width, thickness).cutBlind(w_height) # No that's perpendicular
    
    # Let's stick to Workplane and rect/cut
    
    # Re-instantiate
    part = cq.Workplane("XY").box(width, height, thickness)
    
    # 1. Cut the main window
    window_height = height - top_frame_width - (bottom_rail_height + leg_height)
    window_width = width - 2 * side_frame_width
    
    # Calculate offset from center for the window
    # The solid material at the top is 'top_frame_width'
    # The solid material at the bottom is 'bottom_rail_height + leg_height'
    # Current Y center is 0. Top is H/2, Bottom is -H/2.
    # Top of window = H/2 - top_frame_width
    # Bottom of window = -H/2 + bottom_rail_height + leg_height
    # Center Y of window = (Top_of_window + Bottom_of_window) / 2
    window_center_y = ((height/2 - top_frame_width) + (-height/2 + bottom_rail_height + leg_height)) / 2
    
    part = part.faces(">Z").workplane().center(0, window_center_y).rect(window_width, window_height).cutBlind(-thickness)
    
    # 2. Cut the bottom notch between legs
    # The notch is at the bottom, creating the feet.
    # It effectively removes material from y = -H/2 to y = -H/2 + leg_height
    # The width matches the window width usually for these types of frames? 
    # Looking at the image, the inner vertical edge seems continuous from the window down to the floor.
    # So the notch width is the same as the window width.
    
    notch_height = leg_height
    notch_width = window_width
    
    # Center Y of notch = -H/2 + notch_height/2
    notch_center_y = -height/2 + notch_height/2
    
    # We need to reset the center from the previous operation, workplane() creates a new one based on the face but center() shifts it
    # It's safer to grab the face again or use the stack correctly.
    
    part = part.faces(">Z").workplane().center(0, notch_center_y).rect(notch_width, notch_height).cutBlind(-thickness)
    
    return part

result = create_frame()