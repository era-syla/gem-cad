import cadquery as cq

# Parameters for the main body
base_width = 140.0
base_height = 12.0
depth = 25.0
top_width = 30.0
total_height = 80.0
flange_inner_x = 35.0

# Define the front profile points of the block
pts = [
    (-base_width / 2, 0),
    (base_width / 2, 0),
    (base_width / 2, base_height),
    (flange_inner_x, base_height),
    (top_width / 2, total_height),
    (-top_width / 2, total_height),
    (-flange_inner_x, base_height),
    (-base_width / 2, base_height)
]

# Create the main trapezoidal flanged body
main_body = cq.Workplane("XY").polyline(pts).close().extrude(depth)

# Parameters for the channel
channel_width = 14.0
channel_depth = 12.0

# Create a tool to cut the front channel
channel = (
    cq.Workplane("XY", origin=(0, total_height / 2, depth - channel_depth))
    .rect(channel_width, total_height + 10)
    .extrude(channel_depth + 10)
)

result = main_body.cut(channel)

# Parameters for the holes
hole_dia = 6.0
num_holes = 5
hole_spacing = 11.0
start_y = 28.0

# Calculate the center points for the holes
hole_centers = [(0, start_y + i * hole_spacing) for i in range(num_holes)]

# Create and cut the holes
holes = (
    cq.Workplane("XY", origin=(0, 0, -5))
    .pushPoints(hole_centers)
    .circle(hole_dia / 2)
    .extrude(depth + 10)
)

result = result.cut(holes)