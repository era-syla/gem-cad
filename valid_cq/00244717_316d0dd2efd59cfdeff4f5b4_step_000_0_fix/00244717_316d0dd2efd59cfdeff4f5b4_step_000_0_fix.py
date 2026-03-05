import cadquery as cq

# Parameters
plate_length = 120
plate_width = 80
plate_thickness = 3
tab_length = 40
tab_width = 30
pocket_length = 80
pocket_width = 50
pocket_depth = 2
hole_dia = 10
boss_size = 6
boss_height = pocket_depth
boss_positions = [(-30, 10), (-10, 10), (10, 10), (30, 10), (-10, -10), (30, -10)]
rail_width = 3
rail_height = pocket_depth
rail_length = pocket_length - 10
rail_ys = [pocket_width/2 - rail_width/2, -(pocket_width/2 - rail_width/2)]
post_dia = 5
post_height = 5
post_offset = 5
post_x_offset = pocket_length/2 - post_offset
post_y_offset = pocket_width/2 - post_offset
post_positions = [
    (-post_x_offset, post_y_offset),
    (post_x_offset, post_y_offset),
    (post_x_offset, -post_y_offset),
    (-post_x_offset, -post_y_offset),
]

# Create main plate and tab
main = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)
tab = (
    cq.Workplane("XY")
    .transformed(offset=(-(plate_length/2 + tab_length/2), 0, 0))
    .box(tab_length, tab_width, plate_thickness)
)
plate = main.union(tab)

# Pocket cut in top face
plate = plate.faces(">Z").workplane().rect(pocket_length, pocket_width).cutBlind(-pocket_depth)

# Hole in tab
hole_x = -(plate_length/2 + tab_length/2)
plate = (
    plate.faces(">Z")
    .workplane()
    .transformed(offset=(hole_x, 0, 0))
    .circle(hole_dia / 2)
    .cutBlind(plate_thickness)
)

# Add bosses inside pocket
for x, y in boss_positions:
    plate = (
        plate.faces(">Z")
        .workplane()
        .transformed(offset=(x, y))
        .rect(boss_size, boss_size)
        .extrude(boss_height)
    )

# Add guide rails along pocket sides
for y in rail_ys:
    plate = (
        plate.faces(">Z")
        .workplane()
        .transformed(offset=(0, y))
        .rect(rail_length, rail_width)
        .extrude(rail_height)
    )

# Add posts below pocket corners
for x, y in post_positions:
    plate = (
        plate.faces("<Z")
        .workplane()
        .transformed(offset=(x, y))
        .circle(post_dia / 2)
        .extrude(-post_height)
    )

result = plate