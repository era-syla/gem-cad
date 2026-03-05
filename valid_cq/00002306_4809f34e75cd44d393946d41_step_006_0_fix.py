import cadquery as cq

# Main base plate
base_length = 80
base_width = 50
base_height = 6

# Middle platform
mid_length = 70
mid_width = 40
mid_height = 4

# Top pads (square bases for the cylinders)
pad_size = 22
pad_height = 4

# Cylinder dimensions
cyl_outer_r = 9
cyl_inner_r = 6
cyl_height = 12

# Spacing between the two bosses
boss_x_offset = 20

# Build base plate
result = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_height, centered=(True, True, False))
)

# Add middle raised platform on top of base
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(mid_length, mid_width)
    .extrude(mid_height)
)

# Add two square pads on top of the middle platform
# Left pad
result = (
    result
    .faces(">Z")
    .workplane()
    .center(-boss_x_offset, 0)
    .rect(pad_size, pad_size)
    .extrude(pad_height)
)

# Right pad
result = (
    result
    .faces(">Z")
    .workplane()
    .center(boss_x_offset, 0)
    .rect(pad_size, pad_size)
    .extrude(pad_height)
)

# Add left cylinder boss
result = (
    result
    .faces(">Z")
    .workplane()
    .center(-boss_x_offset, 0)
    .circle(cyl_outer_r)
    .extrude(cyl_height)
)

# Add right cylinder boss
result = (
    result
    .faces(">Z")
    .workplane()
    .center(boss_x_offset, 0)
    .circle(cyl_outer_r)
    .extrude(cyl_height)
)

# Cut holes through both cylinders
# Left hole
result = (
    result
    .faces(">Z")
    .workplane()
    .center(-boss_x_offset, 0)
    .circle(cyl_inner_r)
    .cutThruAll()
)

# Right hole
result = (
    result
    .faces(">Z")
    .workplane()
    .center(boss_x_offset, 0)
    .circle(cyl_inner_r)
    .cutThruAll()
)

# Add side rails/channels on the long sides of the base plate
# These appear as stepped features on the sides
rail_height = 3
rail_width = 5

# Left rail (negative Y side)
result = (
    result
    .faces(">Z[-3]")
    .workplane()
    .center(0, -(mid_width/2 + rail_width/2))
    .rect(mid_length, rail_width)
    .extrude(rail_height)
)

# Right rail (positive Y side)
result = (
    result
    .faces(">Z[-3]")
    .workplane()
    .center(0, (mid_width/2 + rail_width/2))
    .rect(mid_length, rail_width)
    .extrude(rail_height)
)

# Cut a small notch/channel in the middle of the right side for the connector feature
result = (
    result
    .faces(">Y")
    .workplane()
    .center(0, base_height/2 + mid_height/2)
    .rect(8, mid_height + rail_height)
    .cutThruAll()
)