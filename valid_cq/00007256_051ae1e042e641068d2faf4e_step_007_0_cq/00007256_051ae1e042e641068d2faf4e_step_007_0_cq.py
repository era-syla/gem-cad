import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the main wall/plate
wall_width = 100.0   # Total width
wall_height = 100.0  # Total height
thickness = 5.0      # Thickness of the plate

# Dimensions of the cutout (doorway shape)
cutout_width = 25.0
cutout_height = 50.0

# Position of the cutout relative to the bottom right
# It seems to be inset slightly from the right edge based on typical design patterns, 
# but looking closely at the image, there is a thin leg on the right.
# Let's parameterize the "leg" width on the right side.
right_leg_width = 10.0 

# --- Modeling Strategy ---
# 1. Create a base rectangular box representing the full wall.
# 2. Create a box representing the cutout.
# 3. Position the cutout box.
# 4. Subtract the cutout from the main wall.

# Create the main body
# We anchor at Center for X/Y to make symmetric operations easier if needed, 
# but for this specific shape, anchoring corners might be more intuitive. 
# Let's stick to center and calculating offsets.
base = cq.Workplane("XY").box(wall_width, wall_height, thickness)

# Calculate the center position for the cutout
# The cutout is at the bottom, so its Y center needs to be:
# -wall_height/2 + cutout_height/2
# The cutout is on the right side, leaving a 'right_leg_width'.
# The right edge of the wall is at +wall_width/2.
# So the right edge of the cutout is at (+wall_width/2) - right_leg_width.
# The center of the cutout in X is (Right_Edge - cutout_width/2).
cutout_x_center = (wall_width / 2) - right_leg_width - (cutout_width / 2)
cutout_y_center = -(wall_height / 2) + (cutout_height / 2)

# Create the cutout geometry
# We make the cutout slightly thicker than the wall to ensure a clean cut
cutout = (
    cq.Workplane("XY")
    .center(cutout_x_center, cutout_y_center)
    .box(cutout_width, cutout_height, thickness * 2)
)

# Perform the boolean cut operation
result = base.cut(cutout)

# Export the result (optional but good practice for verification if running locally)
# cq.exporters.export(result, "wall_with_cutout.step")