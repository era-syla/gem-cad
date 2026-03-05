import cadquery as cq

# --- Parameters ---
# Frame dimensions
frame_length = 140.0
frame_width = 90.0
frame_height = 15.0
frame_thickness = 2.0

# Cross member dimensions (T-profile)
cross_flange_width = 10.0   # Width of the top horizontal part
cross_flange_thick = 1.5    # Thickness of the top horizontal part
cross_web_thick = 1.5       # Thickness of the vertical web
gap = 5.0                   # Clearance gap between cross and frame
web_setback = 5.0           # Distance the web stops before the flange end (notch effect)

# --- Geometry Generation ---

# 1. Create the outer rectangular frame
# We draw the outer boundary, the inner boundary, and extrude.
frame = (
    cq.Workplane("XY")
    .rect(frame_length, frame_width)
    .rect(frame_length - 2*frame_thickness, frame_width - 2*frame_thickness)
    .extrude(frame_height)
)

# 2. Create the inner cross structure
# The cross consists of two beams with a T-profile (Flat flange on top, vertical web below).
# We construct them by unioning separate boxes for flanges and webs.

# Calculate lengths for the cross arms based on frame size and gap
arm_x_len = frame_length - 2 * gap
arm_y_len = frame_width - 2 * gap

# Z-height for the center of the flange (aligned with top of frame)
flange_z_center = frame_height - (cross_flange_thick / 2.0)

# Create the top flanges (Horizontal bars)
flange_x = (
    cq.Workplane("XY")
    .workplane(offset=flange_z_center)
    .box(arm_x_len, cross_flange_width, cross_flange_thick)
)

flange_y = (
    cq.Workplane("XY")
    .workplane(offset=flange_z_center)
    .box(cross_flange_width, arm_y_len, cross_flange_thick)
)

# Create the webs (Vertical bars)
# Webs are shorter than flanges to create the characteristic notched ends
web_len_x = arm_x_len - 2 * web_setback
web_len_y = arm_y_len - 2 * web_setback
web_height = frame_height - cross_flange_thick

# Web aligned with X axis
web_x = (
    cq.Workplane("XY")
    .box(web_len_x, cross_web_thick, web_height, centered=(True, True, False))
)

# Web aligned with Y axis
web_y = (
    cq.Workplane("XY")
    .box(cross_web_thick, web_len_y, web_height, centered=(True, True, False))
)

# 3. Combine all parts into the final result
result = (
    frame
    .union(flange_x)
    .union(flange_y)
    .union(web_x)
    .union(web_y)
)