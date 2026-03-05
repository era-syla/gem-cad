import cadquery as cq

# Define parametric dimensions for the part
height = 50.0
total_width = 80.0
thickness = 15.0
chamfer_size = 20.0

# Define feature specific dimensions
left_block_width = 25.0
leg_bottom_y = -15.0
leg_bottom_width = 10.0
right_vertical_segment = 15.0
notch_peak_x = 35.0
notch_peak_y = 15.0

# Calculate vertices coordinates
# Starting from origin (0,0) at the bottom-left corner of the main block
p1 = (0, 0)
p2 = (0, height)
p3 = (total_width - chamfer_size, height)
p4 = (total_width, height - chamfer_size)
p5 = (total_width, height - chamfer_size - right_vertical_segment)
# Determine x-coordinate for outer leg based on visual proportions
leg_outer_x = 65.0 
p6 = (leg_outer_x, leg_bottom_y)
p7 = (leg_outer_x - leg_bottom_width, leg_bottom_y)
p8 = (notch_peak_x, notch_peak_y)
p9 = (left_block_width, 0)

# Create the profile points list
points = [p1, p2, p3, p4, p5, p6, p7, p8, p9]

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)