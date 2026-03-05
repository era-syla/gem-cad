import cadquery as cq

# Base plate dimensions
base_size = 80
base_height = 10
corner_radius = 8

# Cube dimensions
cube_size = 28
cube_height = 28
cube_offset = 16  # distance from center to cube center

# Gap between cubes (for the cross channel)
gap = 8

# Create the base plate with rounded corners
base = (
    cq.Workplane("XY")
    .rect(base_size, base_size)
    .extrude(base_height)
)

# Round the corners of the base
base = base.edges("|Z").fillet(corner_radius)

# Create the four corner cubes
cube_positions = [
    (cube_offset, cube_offset),
    (-cube_offset, cube_offset),
    (-cube_offset, -cube_offset),
    (cube_offset, -cube_offset),
]

# Add each cube on top of the base
for pos in cube_positions:
    base = (
        base
        .faces(">Z")
        .workplane()
        .center(pos[0], pos[1])
        .rect(cube_size, cube_size)
        .extrude(cube_height)
    )

# Now we need to create the cross-shaped channel between the cubes
# The channel cuts through the top of the base and between the cubes
# It's a plus/cross shape in the center

channel_width = gap
channel_depth = cube_height + base_height

# Cut horizontal channel
base = (
    base
    .faces(">Z")
    .workplane(offset=-channel_depth)
    .center(0, 0)
    .rect(base_size + 10, channel_width)
    .cutBlind(channel_depth)
)

# Cut vertical channel
base = (
    base
    .faces(">Z")
    .workplane(offset=-channel_depth)
    .center(0, 0)
    .rect(channel_width, base_size + 10)
    .cutBlind(channel_depth)
)

# Add rounded fillet to the inside corners of the cross channel
# Add a cylindrical post in the center bottom of the cross to create rounded effect
center_cylinder = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(0, 0)
    .circle(channel_width / 2)
    .extrude(base_height)
)

# Union the center rounded part
base = base.union(center_cylinder)

# Fillet top edges of the cubes slightly
base = base.edges(">Z").fillet(1.5)

result = base