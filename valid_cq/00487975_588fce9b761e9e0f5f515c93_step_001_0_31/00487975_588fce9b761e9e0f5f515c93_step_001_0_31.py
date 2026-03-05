import cadquery as cq
import math

# Define parameters for the model
length = 100.0
width = 60.0
height_base = 15.0
height_left = 25.0
height_right = 35.0

cutout_radius = 10.0
cutout_start_x = 10.0
cutout_end_x = cutout_start_x + 2 * cutout_radius  # 30.0

curve_radius = 20.0
curve_start_x = 50.0
curve_end_x = curve_start_x + curve_radius  # 70.0

# Calculate midpoint for the semi-circle cutout (lowest point)
arc1_mid_x = cutout_start_x + cutout_radius
arc1_mid_z = height_left - cutout_radius

# Calculate midpoint for the quarter-circle curve (at 45 degrees)
arc2_mid_x = curve_start_x + curve_radius * math.cos(math.pi / 4)
arc2_mid_z = height_base + curve_radius * math.sin(math.pi / 4)

# Build the 2D profile on the XZ plane and extrude
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, height_left)
    .lineTo(cutout_start_x, height_left)
    .threePointArc((arc1_mid_x, arc1_mid_z), (cutout_end_x, height_left))
    .lineTo(cutout_end_x, height_right)
    .lineTo(curve_start_x, height_right)
    .threePointArc((arc2_mid_x, arc2_mid_z), (curve_end_x, height_base))
    .lineTo(length, height_base)
    .lineTo(length, 0)
    .close()
    .extrude(width)
)