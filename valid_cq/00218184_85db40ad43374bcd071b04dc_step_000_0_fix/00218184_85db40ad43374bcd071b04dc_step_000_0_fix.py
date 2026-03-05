import cadquery as cq

# Parameters
length = 140
width = 40
height = 20

pocket_len = 50
pocket_wid = 20
pocket_depth = 5

post_size = 4
post_height = 15

# Build main body
result = cq.Workplane("XY").box(length, width, height)

# Cut central top pocket
result = result.faces(">Z").workplane().rect(pocket_len, pocket_wid).cutBlind(-pocket_depth)

# Fillet front/back vertical edges to approximate curved ramps
result = result.edges("<X or >X").fillet(8)

# Add two vertical posts on top of the pocket
post_x_positions = (-pocket_len/2 + post_size/2, pocket_len/2 - post_size/2)
for x in post_x_positions:
    result = (
        result.faces(">Z")
        .workplane(centerOption="CenterOfMass")
        .transformed(offset=(x, 0, 0))
        .rect(post_size, post_size)
        .extrude(post_height)
    )