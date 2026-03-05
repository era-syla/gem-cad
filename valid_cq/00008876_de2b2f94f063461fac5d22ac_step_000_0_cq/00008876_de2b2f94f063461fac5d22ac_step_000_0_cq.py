import cadquery as cq

# Parameters for the design
thickness = 2.0  # Thickness of the plate
main_body_width = 40.0
main_body_length = 60.0

# Dimensions for the "U" shaped cutout at the back
cutout_width = 20.0
cutout_depth = 15.0

# Dimensions for the side squares (diamond shape lobes)
side_square_size = 30.0
connection_offset_x = 10.0 # How far the connection point is from center

# Create the main central body
# We start with a rectangle
main_body = cq.Workplane("XY").box(main_body_length, main_body_width, thickness)

# Create the cutout at the 'back' (negative X direction in this orientation)
# We move to the face, draw a rectangle and cut it
cutout = (
    cq.Workplane("XY")
    .moveTo(-main_body_length/2, 0)
    .rect(cutout_depth * 2, cutout_width) # Double depth to ensure full cut from edge
    .extrude(thickness)
)

# Subtract the cutout from the main body
central_part = main_body.cut(cutout)

# Now creates the two diagonal squares attached to the front corners
# Based on the image, these seem to be squares rotated by 45 degrees or attached at a corner point.
# Let's model them as separate squares translated to the correct position.
# Looking closely at the vertex connections, the squares touch the corners of the main body.

# Calculate position for the "right" square (in image perspective)
# It attaches to the corner at (main_body_length/2, -main_body_width/2)
right_square_center_x = main_body_length/2 + side_square_size/2
right_square_center_y = -main_body_width/2 - side_square_size/2

right_square = (
    cq.Workplane("XY")
    .center(right_square_center_x, right_square_center_y)
    .box(side_square_size, side_square_size, thickness)
)

# Calculate position for the "left" square (in image perspective)
# It attaches to the corner at (main_body_length/2, main_body_width/2)
left_square_center_x = main_body_length/2 + side_square_size/2
left_square_center_y = main_body_width/2 + side_square_size/2

left_square = (
    cq.Workplane("XY")
    .center(left_square_center_x, left_square_center_y)
    .box(side_square_size, side_square_size, thickness)
)

# Combine all parts
result = central_part.union(right_square).union(left_square)

# To strictly match the image orientation where the "U" shape is to the left/top
# and the squares are to the right/bottom:
result = result.rotate((0,0,0), (0,0,1), 45)