import cadquery as cq

length = 100
width = 10
height = 10
bottom_thickness = 4
channel_width = 6
channel_length = 15
channel_height = height - bottom_thickness
chamfer_size = 4
slot_width = 1
slot_height = 3
slot_depth = 2

result = cq.Workplane("XY").box(length, width, height)

# Cut the U-shaped channel at the front
z_center = -height/2 + bottom_thickness + channel_height/2
result = result.faces(">X").workplane().center(0, z_center) \
    .rect(channel_width, channel_height).cutBlind(channel_length)

# Chamfer the top front edge corners
result = result.edges(">X").edges(">Z").chamfer(chamfer_size)

# Add the rectangular slot on the side
result = result.faces(">Y").workplane() \
    .rect(slot_width, slot_height).cutBlind(slot_depth)