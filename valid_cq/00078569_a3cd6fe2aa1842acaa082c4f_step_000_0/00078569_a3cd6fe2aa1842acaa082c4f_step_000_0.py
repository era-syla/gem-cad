import cadquery as cq
import math

# --- Parameters ---
# Overall dimensions of the frame
total_height = 100.0      # Vertical height from ground to top of legs
base_spread = 60.0        # Horizontal distance between leg centers at the bottom
top_spread = 40.0         # Horizontal distance between leg centers at the top

# Profile dimensions
beam_size = 5.0           # Width/Depth of the square profile for legs and crossbar
crossbar_offset = 15.0    # Distance from the top of the legs to the center of the crossbar

# --- Calculations ---
# Calculate the slant geometry
delta_x = (base_spread - top_spread) / 2.0
slant_angle = math.degrees(math.atan2(delta_x, total_height))
leg_length = math.sqrt(total_height**2 + delta_x**2)

# Calculate placement coordinates
# The center of the leg in X is the average of the top and bottom radii
leg_center_x = (base_spread + top_spread) / 4.0
leg_center_z = total_height / 2.0

# --- Modeling ---

# 1. Create the Right Leg
# We create a beam centered at the origin, rotate it, and then move it into position
right_leg = (
    cq.Workplane("XY")
    .box(beam_size, beam_size, leg_length)
    .rotate((0, 0, 0), (0, 1, 0), -slant_angle) # Rotate around Y-axis
    .translate((leg_center_x, 0, leg_center_z))
)

# 2. Create the Left Leg by mirroring the Right Leg across the YZ plane
left_leg = right_leg.mirror("YZ")

# 3. Create the Crossbar
# Determine the Z height for the crossbar
crossbar_z = total_height - crossbar_offset

# Calculate the width between leg centerlines at the specific height of the crossbar
# Using linear interpolation based on the slope of the legs
slope = ((top_spread - base_spread) / 2.0) / total_height
current_half_width = (slope * crossbar_z) + (base_spread / 2.0)
crossbar_length = current_half_width * 2.0

crossbar = (
    cq.Workplane("XY")
    .box(crossbar_length, beam_size, beam_size) # Length (X), Depth (Y), Height (Z)
    .translate((0, 0, crossbar_z))
)

# 4. Combine all parts into a single object
result = right_leg.union(left_leg).union(crossbar)