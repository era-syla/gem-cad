import cadquery as cq

# -- Parametric Dimensions --
length = 140.0          # Total length of the blade
base_height = 40.0      # Height at the wide end (right)
tip_height = 10.0       # Height at the narrow tip (left)
tip_lift = 12.0         # Vertical offset of the tip from the base bottom
thickness = 15.0        # Extrusion thickness
belly_sag = 8.0         # Convexity depth of the bottom curve
num_teeth = 9           # Number of serrations
tooth_depth = 5.0       # Depth of the vertical drop of each tooth

# Attachment/Mount parameters
mount_len = 12.0        # Length of the protruding block
mount_h = 24.0          # Height of the block (Y direction)
mount_w = 10.0          # Width/Thickness of the block (Z direction)
chamfer_val = 2.0       # Size of the chamfer at the end

# -- Model Construction --

# Define Key Coordinates (XY Plane)
# Origin (0,0) is at the bottom-right corner of the main body
p_start = (0, 0)
p_tip_btm = (-length, tip_lift)
p_tip_top = (-length, tip_lift + tip_height)
p_base_top = (0, base_height)

# Calculate mid-point for the bottom arc (convex shape)
mid_x = -length / 2
# Linear midpoint Y between start and tip_btm minus sag
mid_y = (p_start[1] + p_tip_btm[1]) / 2 - belly_sag
p_arc_mid = (mid_x, mid_y)

# Initialize Sketch on XY Plane
# 1. Draw bottom arc
# 2. Draw vertical tip face
sketch = (
    cq.Workplane("XY")
    .moveTo(*p_start)
    .threePointArc(p_arc_mid, p_tip_btm)
    .lineTo(*p_tip_top)
)

# 3. Generate Sawtooth Pattern
# Interpolate between tip top and base top
dx = length / num_teeth
y_range = p_base_top[1] - p_tip_top[1]

for i in range(num_teeth):
    # Calculate Peak coordinates
    # We move from left (-length) to right (0)
    step_idx = i + 1
    peak_x = -length + (step_idx * dx)
    
    # Linear height interpolation for the peak
    peak_y = p_tip_top[1] + (y_range * (step_idx / num_teeth))
    
    # Draw slope up to the peak
    sketch = sketch.lineTo(peak_x, peak_y)
    
    # Draw the vertical drop (the "bite" of the tooth)
    # Skip for the last tooth as it connects directly to the back face
    if i < num_teeth - 1:
        sketch = sketch.lineTo(peak_x, peak_y - tooth_depth)

# 4. Close the sketch (connects last peak to (0,0))
sketch = sketch.close()

# 5. Extrude Main Body
body = sketch.extrude(thickness)

# 6. Add Mounting Block
# Select the flat face at the base (X=0 plane)
# workplane() on a >X face typically aligns local X with global Y
# We draw a centered rectangle. 
# Width corresponds to Global Y (Height), Height corresponds to Global Z (Thickness)
result = (
    body.faces(">X")
    .workplane()
    .rect(mount_h, mount_w)
    .extrude(mount_len)
)

# 7. Chamfer the end of the mount
# Select the new face at the extreme +X and chamfer its edges
result = result.faces(">X").edges().chamfer(chamfer_val)

# Return the final object