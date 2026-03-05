import cadquery as cq

# Base dimensions
length = 100
width = 50
height = 15

# Create base block
result = cq.Workplane("XY").box(length, width, height)

# Add cylindrical posts on top face
post_radius = 3
post_height = 8
post_positions = [(-40, -20), (40, 20)]
for x, y in post_positions:
    result = result.faces(">Z").workplane().center(x, y).circle(post_radius).extrude(post_height)

# Create a circular bowl pocket
circle_center = (15, 0)
circle_radius = 10
bowl_depth = 6
result = result.faces(">Z").workplane().center(*circle_center).circle(circle_radius).cutBlind(bowl_depth)

# Create a straight channel pocket leading to the left edge
channel_width = 6
channel_length = 60
channel_depth = 5
# Position the channel so it starts tangent to the circle and extends left
channel_start_x = circle_center[0] - circle_radius - channel_length/2
result = result.faces(">Z").workplane().center(channel_start_x, 0).rect(channel_length, channel_width).cutBlind(channel_depth)

# Create a small rectangular notch at the top of the bowl
notch_width = 12
notch_height = 4
notch_depth = 2
notch_center = (circle_center[0] - notch_width/2, circle_center[1] + circle_radius)
result = result.faces(">Z").workplane().center(*notch_center).rect(notch_width, notch_height).cutBlind(notch_depth)