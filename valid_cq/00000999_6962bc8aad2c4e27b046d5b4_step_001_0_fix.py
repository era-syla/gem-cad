import cadquery as cq

# Main base block
base_length = 200
base_width = 60
base_height = 20

# Create the main base
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# Create two rail channels on top (running along X axis)
# Left channel
channel_width = 8
channel_depth = 8
channel_offset = 15

left_channel = (
    cq.Workplane("XY")
    .transformed(offset=(0, channel_offset, base_height/2 - channel_depth/2))
    .box(base_length, channel_width, channel_depth)
)

right_channel = (
    cq.Workplane("XY")
    .transformed(offset=(0, -channel_offset, base_height/2 - channel_depth/2))
    .box(base_length, channel_width, channel_depth)
)

# Cut channels from base
result = base.cut(left_channel).cut(right_channel)

# Add raised rails on top between and outside channels
rail_height = 15
rail_width = 12

# Center rail (between channels)
center_rail = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, base_height/2 + rail_height/2))
    .box(base_length, rail_width, rail_height)
)

# Left outer rail
left_rail = (
    cq.Workplane("XY")
    .transformed(offset=(0, 28, base_height/2 + rail_height/2))
    .box(base_length, rail_width, rail_height)
)

# Right outer rail
right_rail = (
    cq.Workplane("XY")
    .transformed(offset=(0, -28, base_height/2 + rail_height/2))
    .box(base_length, rail_width, rail_height)
)

result = result.union(center_rail).union(left_rail).union(right_rail)

# Add holes along the top surface of rails
# Holes on center rail
hole_positions_x = [-80, -60, -40, -20, 0, 20, 40, 60, 80]
hole_diameter = 3
hole_depth = 10

for x_pos in hole_positions_x:
    result = result.faces(">Z").workplane().center(x_pos, 0).hole(hole_diameter, hole_depth)

# Holes on left rail
for x_pos in hole_positions_x[::2]:
    result = (
        result
        .faces(">Z")
        .workplane()
        .center(x_pos, 28)
        .hole(hole_diameter, hole_depth)
    )

# Holes on right rail
for x_pos in hole_positions_x[::2]:
    result = (
        result
        .faces(">Z")
        .workplane()
        .center(x_pos, -28)
        .hole(hole_diameter, hole_depth)
    )

# Add end connector blocks on each end
connector_width = 20
connector_height = base_height + rail_height
connector_depth = 15

left_connector = (
    cq.Workplane("XY")
    .transformed(offset=(-base_length/2 - connector_depth/2, 0, connector_height/2 - base_height/2))
    .box(connector_depth, connector_width, connector_height)
)

right_connector = (
    cq.Workplane("XY")
    .transformed(offset=(base_length/2 + connector_depth/2, 0, connector_height/2 - base_height/2))
    .box(connector_depth, connector_width, connector_height)
)

result = result.union(left_connector).union(right_connector)

# Add holes in connector blocks (side holes)
# Left connector holes
result = (
    result
    .faces("<X")
    .workplane()
    .pushPoints([(0, 5), (0, -5)])
    .hole(3, 10)
)

# Right connector holes  
result = (
    result
    .faces(">X")
    .workplane()
    .pushPoints([(0, 5), (0, -5)])
    .hole(3, 10)
)

# Add small bolt holes on the sides of the base
result = (
    result
    .faces("<Y")
    .workplane()
    .pushPoints([(-70, 0), (0, 0), (70, 0)])
    .hole(3, 8)
)

result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints([(-70, 0), (0, 0), (70, 0)])
    .hole(3, 8)
)