import cadquery as cq

# Parameters
plate_length = 120
plate_width = 80
base_thickness = 3
shelf_length = 80
shelf_width = 50
shelf_thickness = 2
central_pocket_size = (50, 30)
central_pocket_depth = 1
square_hole_size = (20, 20)
square_hole_pos = (30, 15)
small_pocket_size = (15, 20)
small_pocket_depth = 2
small_pocket_positions = [(20, -15), (40, -15)]

# Base plate
result = cq.Workplane("XY").rect(plate_length, plate_width).extrude(base_thickness)

# Shelf on top left
shelf_x = -plate_length/2 + shelf_length/2
shelf_y =  plate_width/2 - shelf_width/2
result = (
    result
    .faces(">Z")
    .workplane(origin=(shelf_x, shelf_y))
    .rect(shelf_length, shelf_width)
    .extrude(shelf_thickness)
)

# Central recessed pocket
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(*central_pocket_size)
    .cutBlind(central_pocket_depth)
)

# Through square hole at top right
result = (
    result
    .faces(">Z")
    .workplane(origin=square_hole_pos)
    .rect(*square_hole_size)
    .cutThruAll()
)

# Two small bottom-right pockets
for pos in small_pocket_positions:
    result = (
        result
        .faces(">Z")
        .workplane(origin=pos)
        .rect(*small_pocket_size)
        .cutBlind(small_pocket_depth)
    )