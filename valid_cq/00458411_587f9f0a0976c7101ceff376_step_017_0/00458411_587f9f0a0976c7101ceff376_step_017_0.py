import cadquery as cq

# Parametric dimensions for the shaft
total_length = 350.0
main_diameter = 12.0

# Left end configuration (Front-left in view)
# Tip section
left_tip_diameter = 6.0
left_tip_length = 8.0
# Intermediate step section
left_step_diameter = 10.0
left_step_length = 15.0
# Groove parameters (for retaining ring on the intermediate step)
groove_width = 1.2
groove_depth = 0.5
groove_margin = 4.0 # Distance from the start of the step

# Right end configuration (Back-right in view)
right_step_diameter = 10.0
right_step_length = 12.0

# Derived dimensions
main_radius = main_diameter / 2.0
left_tip_radius = left_tip_diameter / 2.0
left_step_radius = left_step_diameter / 2.0
right_step_radius = right_step_diameter / 2.0

# Calculate the length of the main central section
main_length = total_length - (left_tip_length + left_step_length + right_step_length)

# Define the profile points for revolution
# Drawn in XY plane (Y is radial, X is axial)
points = []
current_x = 0.0

# Start at the origin (centerline)
points.append((current_x, 0.0))

# 1. Left Tip
points.append((current_x, left_tip_radius))
current_x += left_tip_length
points.append((current_x, left_tip_radius))

# 2. Left Step with Groove
points.append((current_x, left_step_radius)) # Step up
step_start_x = current_x

# Calculate groove position
groove_start_x = step_start_x + groove_margin
groove_end_x = groove_start_x + groove_width

# Segment before groove
points.append((groove_start_x, left_step_radius))
# Groove down
points.append((groove_start_x, left_step_radius - groove_depth))
# Groove bottom
points.append((groove_end_x, left_step_radius - groove_depth))
# Groove up
points.append((groove_end_x, left_step_radius))

# Remainder of left step
current_x += left_step_length
points.append((current_x, left_step_radius))

# 3. Main Body
points.append((current_x, main_radius)) # Step up to main diameter
current_x += main_length
points.append((current_x, main_radius))

# 4. Right Step
points.append((current_x, right_step_radius)) # Step down
current_x += right_step_length
points.append((current_x, right_step_radius))

# Return to centerline
points.append((current_x, 0.0))

# Create the shaft using the revolve operation
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .revolve(360, (0, 0, 0), (1, 0, 0))
)