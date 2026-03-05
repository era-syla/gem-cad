import cadquery as cq

# Parametric dimensions
total_length = 50.0  # Overall length from tip to back
base_width = 15.0    # Width of the main block at the back
base_height = 20.0   # Height of the main block at the back
arm_thickness = 3.0  # Thickness of the tapered arm
tip_width = 2.0      # Width of the tip before the hook
hook_drop = 3.0      # How far down the little hook goes
hook_length = 2.0    # Length of the hook tip
back_relief_cut = 5.0 # Depth of the relief cut on the back

# Create the profile sketch
# We will draw this from the side view (XY plane) and extrude it
# The coordinates are estimated based on visual proportions
pts = [
    (0, 0),                           # Bottom left tip
    (0, -hook_drop),                  # Hook bottom
    (hook_length, -hook_drop),        # Hook inner bottom
    (hook_length, 0),                 # Hook inner corner
    (total_length - 5, 0),            # Start of the base bottom
    (total_length, 0),                # Bottom right corner
    (total_length, base_height),      # Top right corner
    (total_length - 5, base_height),  # Top back edge
    (total_length - 10, base_height + 5), # Angled top feature (peak)
    (total_length - 15, base_height), # Angled top feature (valley/start)
    (hook_length, arm_thickness),     # Top of the tapered arm near tip
    (0, 0)                            # Closing the loop
]

# Create the main body by extruding the side profile
# However, looking closely at the image, the object seems to have a constant thickness
# for the arm but the base is wider. Let's re-evaluate.
# The image shows a complex 3D shape. It's likely easier to build it additively.

# Strategy 2: Build the base block, then the arm, then cut/modify.
# Actually, looking at the top surface, it's uniform.
# The object is essentially a prism (extrusion) with a specific 2D profile.
# Let's trace the 2D profile on the "side" plane (let's say XZ) and extrude along Y.

# Re-defining points for the side profile (XZ plane) based on the image orientation
# Origin at the tip of the hook.
# X is length, Z is height. Extrusion is Y (width).

# Profile Points (Clockwise from tip)
# 1. Tip bottom corner
# 2. Hook downward extension
# 3. Hook bottom
# 4. Hook inner vertical
# 5. Long taper bottom
# 6. Base bottom vertical step
# 7. Base bottom horizontal
# 8. Back vertical
# 9. Top angled surface 1
# 10. Top angled surface peak
# 11. Top angled surface 2
# 12. Top vertical face of base
# 13. Taper top edge back to tip

length = 60.0
height_base = 25.0
width = 10.0
hook_h = 4.0
hook_w = 3.0
arm_tip_h = 2.0

# Let's use a Workplane on XY and extrude Z
# Drawing the profile "flat" as seen from the side
pts = [
    (0, 0),                         # Tip top
    (0, -hook_h),                   # Hook tip bottom
    (hook_w, -hook_h),              # Hook bottom back
    (hook_w, -arm_tip_h),           # Hook inner corner
    (length - 10, -10),             # Bottom of the main slant
    (length - 5, -10),              # Bottom flat section start
    (length, -10),                  # Bottom corner
    (length, 10),                   # Back top corner
    (length - 5, 10),               # Back notch top
    (length - 15, 15),              # Top Peak
    (length - 20, 10),              # Top valley
    (length - 20, 0),               # Front vertical of the tall block part
    (0, 0)                          # Close at tip top
]

# Refining the points to match the specific geometry better
# The geometry has a clear long triangular arm and a blocky base.
# Let's try constructing the profile shown on the "front" face of the object in the image.

x_tip = 0
x_base_start = 40.0
x_end = 50.0

y_tip_top = 0
y_hook_bottom = -3.0
y_arm_bottom_slope_start = -2.0 # Thickness at tip
y_base_bottom = -15.0 # The arm slopes down to here
y_base_top = 15.0 

# Let's adjust coordinate system to match visual "flat on ground" logic better
# Let's sketch on XZ plane.
# Origin at the top-left tip.

result = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),                         # Tip Top-Left
        (0, -5),                        # Hook Tip Bottom
        (3, -5),                        # Hook Bottom Width
        (3, -2),                        # Hook Inner Corner
        (35, -15),                      # Bottom of slope meeting the base
        (45, -15),                      # Bottom of base (slight indent)
        (45, -12),                      # Step up
        (50, -12),                      # Back bottom corner
        (50, 10),                       # Back top corner
        (45, 10),                       # Top step
        (35, 15),                       # Peak of the top feature
        (30, 8),                        # Valley of top feature
        (30, 0),                        # Vertical face connecting to arm
        (0, 0)                          # Close loop
    ])
    .close()
    .extrude(10) # Width of the object
)

# Refine the shape based on the specific "step" look on the right side
# The image shows a flange or separate section on the far right.
# Let's construct it more piecewise to get the details right.

# 1. The main triangular arm
arm_length = 40.0
arm_start_height = 20.0
arm_end_height = 2.0
arm_width = 5.0

# 2. The base block
base_width = 15.0 # Z direction in image (thickness)
base_depth = 15.0 # X direction
base_height = 30.0 # Y direction

# Let's restart with a cleaner profile definition based on vertices
# Viewing from the side (XY plane in CAD, extruding Z)

# Define vertices for the side profile
v1 = (0, 0)             # Tip top
v2 = (0, -3)            # Tip bottom (hook)
v3 = (2, -3)            # Hook back
v4 = (2, -1)            # Hook inner
v5 = (30, -10)          # Bottom slope end
v6 = (40, -10)          # Base bottom forward
v7 = (40, -12)          # Base bottom notch
v8 = (42, -12)          # Base bottom back
v9 = (42, 10)           # Base top back
v10 = (40, 10)          # Base top notch
v11 = (35, 15)          # Top Peak
v12 = (30, 10)          # Top slope start
v13 = (30, 0)           # Connection to arm vertical
v14 = (0, 0)            # Back to start

# Extrusion width
width = 8.0

# Create the main shape
result = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),         # Tip (Top-Left)
        (0, -3),        # Hook drop
        (2.5, -3),      # Hook thickness
        (2.5, -1.5),    # Hook inner ledge
        (35, -12),      # Bottom slope end (meeting base)
        (40, -12),      # Undercut start
        (40, -10),      # Undercut up
        (45, -10),      # Base bottom
        (45, 15),       # Base Back top
        (40, 15),       # Base Top front
        (32, 20),       # Peak
        (25, 15),       # Valley
        (25, 10),       # Vertical drop to arm
        (0, 0)          # Arm top slope (flat in this case)
    ])
    .close()
    .extrude(width)
)

# Looking closer at the image, the arm tapers in width (thickness) as well?
# No, looks like constant extrusion width.

# Wait, there is a distinct vertical line on the base, suggesting a change in depth.
# The "flange" on the right (back of object) might be wider or narrower.
# The image shows a shadow line, implying the back plate is wider than the front arm mechanism.
# Let's adjust.

# Component 1: The Arm and middle block
arm_profile = (
    cq.Workplane("XY")
    .polyline([
        (0, 0), (0, -4), (3, -4), (3, -1.5), # Hook
        (30, -12), # Bottom slope
        (30, 12),  # Vertical interface
        (0, 0)     # Top slope
    ])
    .close()
    .extrude(6)
)

# Component 2: The Base Block
# The base has a complex top shape (peak) and seems to envelop the arm end.
# Let's stick to the single extrusion model first, it's the most robust interpretation of 
# a 2D-looking generated drawing, but let's refine the points to perfectly match the visual.

final_profile = [
    (0, 0),           # 1. Arm Tip (Top)
    (0, -4),          # 2. Hook Tip (Bottom)
    (3, -4),          # 3. Hook Base (Bottom)
    (3, -1.5),        # 4. Hook Inside Corner
    (40, -15),        # 5. Arm Bottom meet Base
    (48, -15),        # 6. Base Bottom corner (slight extension)
    (48, -12),        # 7. Step Up
    (52, -12),        # 8. Back Bottom Corner
    (52, 18),         # 9. Back Top Corner
    (48, 18),         # 10. Step Down/In
    (40, 25),         # 11. Top Peak
    (30, 20),         # 12. Top Valley
    (30, 12),         # 13. Block Vertical Face
    (30, 0),          # 14. Midpoint? No, straight line connection
    (0, 0)            # Close loop
]
# Correction: The top of the arm is flat in the first section of the image, 
# but triangular overall. The image shows a diagonal line from tip to the vertical face of the base.

# Final Coordinate Set Strategy
p_tip = (0, 0)
p_hook_btm = (0, -4)
p_hook_back = (3, -4)
p_hook_throat = (3, -1.5)
p_base_interface_btm = (40, -15)
p_base_corner_btm = (50, -15)
p_base_corner_top = (50, 15)
p_peak = (40, 22)
p_valley = (35, 18)
p_base_interface_top = (35, 10) # Vertical drop
p_arm_top_slope = (0, 0)

# The back part (base) has a "lip" or flange on the very back face.
# Let's simplify to the primary distinct shape which is a single extrusion.

result = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),         # Top tip
        (0, -3),        # Bottom tip
        (2.5, -3),      # Hook bottom width
        (2.5, -1.2),    # Hook throat
        (30, -12),      # Arm bottom end
        (38, -10),      # Base bottom step 1
        (38, -12),      # Base bottom step 2 (down)
        (42, -12),      # Base bottom back
        (42, 12),       # Base top back
        (38, 12),       # Base top step (in)
        (32, 18),       # Peak
        (25, 14),       # Valley/Slope up
        (25, 8),        # Vertical face
        (0, 0)          # Back to tip
    ])
    .close()
    .extrude(6) # Extrusion depth
)