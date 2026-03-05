import cadquery as cq

# --- Parametric Dimensions ---
frame_height = 80.0       # Total height of the frame
frame_width = 50.0        # Total width of the frame
thickness = 10.0          # Thickness (depth) of the model
bar_width = 8.0           # Width of the vertical and horizontal sections
top_offset = 4.0          # How much the top bar is recessed from the top edge

# --- Geometry Calculation ---

# Inner window dimensions
window_width = frame_width - (2 * bar_width)
# Window height: Total height - bottom bar - top bar - top recess
window_height = frame_height - (2 * bar_width) - top_offset

# Y-position for the center of the main window cutout
# The window is shifted downwards due to the top recess
# Top limit: (H/2) - top_offset - bar_width
# Bottom limit: -(H/2) + bar_width
# Center: -top_offset / 2
window_center_y = -top_offset / 2.0

# Y-position for the top notch cutout (the space between the legs at the top)
# Center of the recess area: (H/2) - (recess/2)
notch_center_y = (frame_height / 2.0) - (top_offset / 2.0)

# --- Modeling ---

# 1. Create the base solid block
base = cq.Workplane("XY").box(frame_width, frame_height, thickness)

# 2. Create the cutter for the central window
window_cutter = (
    cq.Workplane("XY")
    .center(0, window_center_y)
    .rect(window_width, window_height)
    .extrude(thickness * 2, both=True) # Ensure it cuts through entirely
)

# 3. Create the cutter for the top recess
notch_cutter = (
    cq.Workplane("XY")
    .center(0, notch_center_y)
    .rect(window_width, top_offset)
    .extrude(thickness * 2, both=True)
)

# 4. Perform boolean operations to create the final shape
result = base.cut(window_cutter).cut(notch_cutter)