import cadquery as cq

# --- Parameters ---
# Ramp dimensions
ramp_radius = 50.0  # Radius of the curved ramp
ramp_width = 40.0   # Width of the ramp surface
ramp_height = 40.0  # Height of the top of the ramp
ramp_length = 50.0  # Horizontal length of the curved section (approx matches radius)
platform_depth = 10.0 # Depth of the top deck

# Frame dimensions
frame_thickness = 1.0  # Thickness of structural members
post_width = 1.5       # Width of vertical posts
num_ribs = 10          # Number of horizontal ribs on the curve
num_posts = 5          # Number of vertical support posts along the curve

# Separate platform (black rectangle in image)
sep_platform_length = 60.0
sep_platform_width = 15.0
sep_platform_height = 1.0
sep_platform_dist = 20.0 # Distance from the ramp

# --- Modeling the Curved Ramp ---

# 1. Create the Profile of the Curve
# We model the side profile first.
# Center of the arc is at (0, ramp_height) if the bottom is at (ramp_length, 0)
# But let's place the corner of the ramp at (0,0) for easier framing.
# A quarter pipe curve usually follows a circular arc.

def ramp_profile(r, h, w):
    # This creates a solid sheet for the surface
    pts = [
        (r, h),           # Top back corner
        (0, h),           # Top front edge
        (0, h - 1),       # Thickness
        (r - 1, h - 1),   # Inner curve start approximate
        (r, 0)            # Bottom edge
    ]
    
    # Let's do it by sweeping a profile or lofting, but a simple extrusion of a 2D sketch is easiest.
    # Sketch approach: 
    # Arc center at (r, h). Start point (0, h). End point (r, 0).
    s = cq.Workplane("YZ") \
        .moveTo(0, h) \
        .radiusArc((r, 0), -r) \
        .lineTo(r + 1, 0) \
        .radiusArc((0 + 1, h), r) \
        .close() \
        .extrude(w)
    return s

# Generate the main curved surface (the "plywood")
# We orient it so width is along X, height Z, length Y
surface = cq.Workplane("YZ").workplane(offset=-ramp_width/2) \
    .moveTo(0, ramp_height) \
    .radiusArc((ramp_length, 0), -ramp_length) \
    .lineTo(ramp_length, -1) \
    .radiusArc((0, ramp_height-1), ramp_length) \
    .close() \
    .extrude(ramp_width)

# 2. Create the Structural Frame
# Side frames (left and right)
def create_side_frame(offset_val):
    frame = cq.Workplane("YZ").workplane(offset=offset_val)
    
    # Top horizontal bar
    top_bar = frame.moveTo(0, ramp_height).lineTo(-platform_depth, ramp_height) \
        .lineTo(-platform_depth, ramp_height - post_width) \
        .lineTo(0, ramp_height - post_width).close().extrude(frame_thickness)
    
    # Vertical posts under the curve
    posts = cq.Workplane("YZ").workplane(offset=offset_val)
    
    # We will place posts at regular intervals along the Y axis
    step = ramp_length / (num_posts - 1)
    
    post_shapes = []
    
    # Back main post
    back_post = frame.rect(post_width, ramp_height + post_width).extrude(frame_thickness) \
        .translate((-post_width/2, ramp_height/2 - post_width/2, frame_thickness/2))
        
    post_shapes.append(back_post)
    
    # Posts under the curve
    for i in range(num_posts):
        y_pos = i * step
        # Calculate height at this Y on the circle: x^2 + y^2 = r^2
        # Here coords are shifted. Center is at (ramp_length, ramp_height) relative to bottom tip? 
        # Let's stick to the arc definition: Center at (ramp_length, ramp_height).
        # Actually, based on previous profile: Center (ramp_length, ramp_height), tip at (0, ramp_height) and (ramp_length, 0).
        # Wait, the previous profile was: Center(ramp_length, ramp_height) is wrong for a standard Q-pipe.
        # Standard Q-pipe: Center is at (Top-Front X, Top-Front Y + R) ?? No.
        # Let's assume curvature:
        # x = 0 is top, x = ramp_length is bottom.
        # Circle center must be at (ramp_length, ramp_height).
        # Equation: (y - ramp_length)^2 + (z - ramp_height)^2 = R^2
        
        # Simpler: Just place vertical pillars and cut them with the curve later? 
        # Easier to calculate height analytically.
        # Curve passes through (0, h) and (L, 0).
        # Using the arc definition from surface creation:
        # Start (0, h), End (L, 0), Radius -L. 
        # Center is at (L, h). 
        # (y - L)^2 + (z - h)^2 = L^2
        
        # We are iterating y_pos from 0 to L.
        # z = h - sqrt(L^2 - (y_pos - L)^2) 
        # Actually (y - L)^2 is same as (L - y)^2.
        
        if y_pos > ramp_length - 0.1: 
            h_curr = 0 # Avoid imaginary numbers at very tip
        else:
            term = ramp_length**2 - (y_pos - ramp_length)**2
            if term < 0: term = 0
            h_curr = ramp_height - (term)**0.5
            
        if h_curr < 2.0: continue # Skip if too short
            
        p = frame.rect(post_width, h_curr).extrude(frame_thickness) \
            .translate((y_pos, h_curr/2, frame_thickness/2))
        post_shapes.append(p)

    # Diagonal Bracing (simplified)
    brace = frame.moveTo(0, ramp_height/2).lineTo(ramp_length/2, 0) \
        .lineTo(ramp_length/2 + post_width, 0).lineTo(0, ramp_height/2 + post_width) \
        .close().extrude(frame_thickness).translate((0,0,0)) # Just a rough brace

    combined_frame = top_bar
    for p in post_shapes:
        combined_frame = combined_frame.union(p)
    
    # Add feet
    feet = frame.rect(post_width * 3, frame_thickness).extrude(frame_thickness) \
         .translate((ramp_length/2, frame_thickness/2, frame_thickness/2)) # Arbitrary foot
    
    return combined_frame

# Create left and right frames
frame_left = create_side_frame(-ramp_width/2)
frame_right = create_side_frame(ramp_width/2 - frame_thickness)

# 3. Create Horizontal Ribs (the "ladder" structure)
ribs = cq.Workplane("YZ")
rib_shapes = []
for i in range(num_ribs):
    # Interpolate along the curve
    t = i / (num_ribs - 1)
    # Angle goes from 90 degrees (top) to 0 degrees (bottom) relative to center
    # Center (L, h). Start (0, h) -> theta = 180. End (L, 0) -> theta = 270?
    # Let's use parametric calc.
    # Angle alpha from 0 to 90 degrees.
    import math
    angle = (math.pi / 2) * t
    
    # Center (ramp_length, ramp_height)
    # x = cx - R * cos(angle) -> y coordinate in our space
    # z = cy - R * sin(angle) -> z coordinate in our space
    # t=0 (top): angle=0. y = L - L(1) = 0. z = h - 0 = h. Correct.
    # t=1 (bot): angle=pi/2. y = L - 0 = L. z = h - L = 0. Correct (assuming h=L).
    
    y_r = ramp_length - ramp_length * math.cos(angle)
    z_r = ramp_height - ramp_length * math.sin(angle)
    
    rib = cq.Workplane("XY").rect(ramp_width, post_width).extrude(frame_thickness) \
        .rotate((0,0,0), (1,0,0), -90 + (t * 90)) \
        .translate((0, y_r, z_r))
        
    rib_shapes.append(rib)

# Combine Ribs
all_ribs = rib_shapes[0]
for r in rib_shapes[1:]:
    all_ribs = all_ribs.union(r)

# 4. Create Top Deck/Platform
top_deck = cq.Workplane("XY").workplane(offset=ramp_height - frame_thickness) \
    .center(0, -platform_depth/2).rect(ramp_width, platform_depth).extrude(frame_thickness)

# 5. Create Separate Platform (The black strip)
# Based on image, it's to the left (negative Y relative to ramp face) or in front. 
# Image: Ramp curves down towards the viewer/right. Strip is on the left.
# Coordinates used: Ramp flows from Y=0 (top) to Y=L (bottom). 
# So "left" of the ramp structure in the image is probably negative X?
# Let's place it aligned with the bottom of the ramp but separated.
sep_platform = cq.Workplane("XY") \
    .rect(sep_platform_width, sep_platform_length) \
    .extrude(sep_platform_height) \
    .translate((-ramp_width - sep_platform_dist, ramp_length/2, 0)) \
    .rotate((0,0,0),(0,0,1), 45) # Rotate to match image perspective slightly better

# 6. Assemble Final Result
# Union everything
ramp_structure = surface.union(frame_left).union(frame_right).union(all_ribs).union(top_deck)
result = ramp_structure.union(sep_platform)
