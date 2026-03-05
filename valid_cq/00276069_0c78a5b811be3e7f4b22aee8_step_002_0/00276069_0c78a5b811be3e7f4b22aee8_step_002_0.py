import cadquery as cq

# Parameter definitions
length = 300.0
width = 150.0
thickness = 20.0
hole_diameter = 12.0

# Margins and spacing
margin_x = 20.0
margin_y = 20.0
left_cluster_spacing = 50.0

# Calculate coordinate values
# Assume plate is centered at (0,0,0) on the XY plane
# X-axis is the long dimension, Y-axis is the short dimension

# Y positions for the rows
y_back = width / 2 - margin_y
y_front = -width / 2 + margin_y

# X positions
x_left_corner = -length / 2 + margin_x
x_left_inset = x_left_corner + left_cluster_spacing
x_right_corner = length / 2 - margin_x

# Middle hole position (back row)
# Placed equidistantly between the left inset hole and the right corner hole
x_mid = (x_left_inset + x_right_corner) / 2

# Define hole coordinates
# Based on visual analysis:
# - Left side has a cluster of holes (Corner + Inset on back edge, Corner on front edge)
# - Right side has a pair of holes (Corner back, Corner front)
# - Middle has a single hole on the back edge
points = [
    (x_left_corner, y_back),   # Back Left Corner
    (x_left_inset, y_back),    # Back Left Inset
    (x_mid, y_back),           # Back Middle
    (x_right_corner, y_back),  # Back Right Corner
    (x_left_corner, y_front),  # Front Left Corner
    (x_right_corner, y_front), # Front Right Corner
]

# Generate the geometry
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(points)
    .hole(hole_diameter)
)