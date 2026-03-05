import cadquery as cq
import math

# --- Parameters ---

# Gear/Knob parameters
num_teeth = 12
gear_outer_diameter = 40.0
gear_height = 20.0
tooth_depth = 5.0
tooth_width_ratio = 0.6 # Ratio of tooth top width to sector width

# Shaft parameters
shaft_diameter = 10.0
top_shaft_length = 15.0
bottom_shaft_length = 20.0

# Slotted head parameters (on top shaft)
slot_width = 2.0
slot_depth = 2.0

# --- Derived Dimensions ---

# Calculate dimensions for the star/gear shape
# We'll construct the profile using polar coordinates or by creating a sketch
radius_outer = gear_outer_diameter / 2.0
radius_inner = radius_outer - tooth_depth

# --- Geometry Construction ---

# 1. Create the Gear/Knob body
# We will create a sketch for the gear profile
# Calculate the angle per tooth
angle_per_tooth = 360.0 / num_teeth
half_angle = angle_per_tooth / 2.0

# Define points for one tooth section
# We need 4 points: inner_left, outer_left, outer_right, inner_right
# The tooth width at the top is determined by a ratio
# Let's use a simpler approach: a polygon constructed from polar coordinates
pts = []
for i in range(num_teeth):
    angle_center = i * angle_per_tooth
    angle_rad = math.radians(angle_center)
    
    # Determine angular span of the outer part of the tooth and the gap
    # Let's say the tooth top takes up 50% of the angle, and the valley takes 50%
    # But looking at the image, the valleys are V-shaped, and the tops are flatish.
    # The image shows flat tops and angled sides going into a small flat bottom valley.
    
    # Let's define specific angles relative to the center of the tooth
    # Tooth Top width (angular)
    alpha = (angle_per_tooth * 0.4) / 2 # Half width of tooth top
    # Valley bottom width (angular)
    beta = (angle_per_tooth * 0.1) / 2  # Half width of valley bottom
    
    # Current tooth center angle
    theta = angle_center 
    
    # Points for one segment (counter-clockwise)
    
    # 1. Start of tooth top (Outer Radius)
    a1 = math.radians(theta - alpha)
    pts.append((radius_outer * math.cos(a1), radius_outer * math.sin(a1)))
    
    # 2. End of tooth top (Outer Radius)
    a2 = math.radians(theta + alpha)
    pts.append((radius_outer * math.cos(a2), radius_outer * math.sin(a2)))
    
    # 3. Start of next valley (Inner Radius) - approximated to midpoint between teeth
    # The valley starts where this tooth ends and goes to where the next tooth starts
    # Let's look at the next segment boundary.
    # The boundary between tooth i and i+1 is at theta + half_angle
    
    # Improved logic based on image:
    # Flat top, angled side, flat bottom (or sharp bottom)
    # The image looks like trapezoidal teeth.
    
    tooth_half_width_angle = (angle_per_tooth * 0.5) / 2.0 # 50% duty cycle for top
    gap_half_angle = (angle_per_tooth - (tooth_half_width_angle*2)) / 2.0
    
    # Point 1: Left side of tooth top
    a_p1 = math.radians(theta + tooth_half_width_angle)
    pts.append((radius_outer * math.cos(a_p1), radius_outer * math.sin(a_p1)))

    # Point 2: Bottom of valley (right side relative to tooth i, left side of gap)
    # The valley is centered at theta + half_angle
    valley_center = theta + half_angle
    
    # Let's make the valley bottom sharp or small flat. Image looks like small flat.
    valley_flat_width_angle = 2.0 # degrees
    
    a_p2 = math.radians(valley_center - valley_flat_width_angle/2)
    pts.append((radius_inner * math.cos(a_p2), radius_inner * math.sin(a_p2)))

    a_p3 = math.radians(valley_center + valley_flat_width_angle/2)
    pts.append((radius_inner * math.cos(a_p3), radius_inner * math.sin(a_p3)))

    # Point 4: Right side of NEXT tooth top is handled in next iteration or we close loop
    # We need to restart the loop logic to be strictly sequential points
    
# Let's rebuild the point list generation to be simpler and strictly sequential
points = []
for i in range(num_teeth):
    center_angle = i * angle_per_tooth
    
    # Ratios for angular widths
    top_ratio = 0.5  # Top of tooth takes 50% of the pitch
    bottom_ratio = 0.1 # Bottom of valley takes 10% of the pitch
    
    # Angles relative to start of sector
    # Sector goes from center_angle - half_angle to center_angle + half_angle
    
    # 1. Left bottom of valley (previous valley)
    # 2. Left top of tooth
    # 3. Right top of tooth
    # 4. Right bottom of valley
    
    # To make it continuous, let's define the profile from -half_angle to +half_angle relative to tooth center
    
    theta_center = center_angle
    
    # Half-widths in degrees
    hw_top = (angle_per_tooth * top_ratio) / 2.0
    hw_bot = (angle_per_tooth * bottom_ratio) / 2.0
    
    # Previous Valley End (Inner Radius)
    # The valley is shared between teeth. 
    # Let's define points for the tooth "island" + the slope to the right.
    
    # Point A: Top Left of Tooth
    pa_ang = math.radians(theta_center - hw_top)
    points.append((radius_outer * math.cos(pa_ang), radius_outer * math.sin(pa_ang)))
    
    # Point B: Top Right of Tooth
    pb_ang = math.radians(theta_center + hw_top)
    points.append((radius_outer * math.cos(pb_ang), radius_outer * math.sin(pb_ang)))
    
    # Point C: Bottom Right Slope (Start of Valley flat)
    valley_center_right = theta_center + (angle_per_tooth/2.0)
    pc_ang = math.radians(valley_center_right - hw_bot)
    points.append((radius_inner * math.cos(pc_ang), radius_inner * math.sin(pc_ang)))
    
    # Point D: Bottom Left Slope (End of Valley flat) - connecting to next tooth
    pd_ang = math.radians(valley_center_right + hw_bot)
    points.append((radius_inner * math.cos(pd_ang), radius_inner * math.sin(pd_ang)))

# Create the gear solid
gear = (cq.Workplane("XY")
        .polyline(points)
        .close()
        .extrude(gear_height))

# 2. Create the Shaft (Upper and Lower)
# The shaft passes through. It's usually one piece.
total_shaft_length = top_shaft_length + gear_height + bottom_shaft_length

# Create a cylinder for the shaft. 
# We center it such that it protrudes correctly.
# Gear is from Z=0 to Z=gear_height.
# Top shaft starts at Z=gear_height, length=top_shaft_length
# Bottom shaft starts at Z=0, goes down by bottom_shaft_length

# Upper Shaft
upper_shaft = (cq.Workplane("XY")
               .workplane(offset=gear_height)
               .circle(shaft_diameter / 2.0)
               .extrude(top_shaft_length))

# Lower Shaft
lower_shaft = (cq.Workplane("XY")
               .circle(shaft_diameter / 2.0)
               .extrude(-bottom_shaft_length))

# 3. Create the Slot in the Top Shaft
# The slot is cut into the top face of the upper shaft
slot_cutter = (cq.Workplane("XY")
               .workplane(offset=gear_height + top_shaft_length)
               .rect(shaft_diameter * 1.5, slot_width) # Make rectangle wider than shaft to cut cleanly
               .extrude(-slot_depth))

# --- Combine Parts ---

# Union the main bodies
result = gear.union(upper_shaft).union(lower_shaft)

# Cut the slot
result = result.cut(slot_cutter)

# Optional: Add fillets to the gear edges as seen in the smooth rendering?
# The image shows fairly sharp edges on the gear profile, but maybe slight fillet on vertical edges.
# The top face of the gear is flat.
# Let's keep it sharp as standard CAD representation unless specifically detailed.
# However, the transition between shaft and gear is sharp in the image.

# Export or Render logic is handled by the environment calling 'result'