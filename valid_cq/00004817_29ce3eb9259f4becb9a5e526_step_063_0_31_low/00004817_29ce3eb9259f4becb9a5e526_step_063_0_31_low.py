import cadquery as cq

# Parameters
base_length = 200.0
base_width = 20.0
base_height = 10.0
groove_width = 5.0
groove_depth = 5.0

plate_length = 100.0
plate_width = 5.0
plate_height_1 = 50.0
plate_height_2 = 100.0
v_depth = 20.0

block_length = 30.0
block_width = 20.0
block_height = 10.0

distance_x = 50.0
distance_y = 50.0

# 1. Base with groove
base = cq.Workplane("XY").box(base_length, base_width, base_height)
groove = cq.Workplane("XY").center(0, 0).box(base_length, groove_width, groove_depth).translate((0, 0, base_height/2 - groove_depth/2))
part1 = base.cut(groove)

# 2. V-shaped plate
pts = [
    (0, 0),
    (plate_length, 0),
    (plate_length, plate_height_2),
    (plate_length/2, plate_height_2 - v_depth),
    (0, plate_height_1)
]

plate = cq.Workplane("XZ").polyline(pts).close().extrude(plate_width).translate((base_length/2 + distance_x, base_width/2 + distance_y, 0))

# 3. Small block
block = cq.Workplane("XY").box(block_length, block_width, block_height).translate((base_length/2 + distance_x + plate_length/2, base_width/2 + distance_y - block_width, block_height/2))


# Combine parts
result = part1.union(plate).union(block)