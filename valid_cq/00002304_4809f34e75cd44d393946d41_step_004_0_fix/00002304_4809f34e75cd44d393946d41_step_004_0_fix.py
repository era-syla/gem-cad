import cadquery as cq

# Parameters
plate_length = 200
plate_width = 80
plate_thickness = 4

tab_length = 15
tab_width = 40
tab_thickness = 4

triangle_side = 10

small_hole_diameter = 3
csk_hole_diameter = 3
csk_diameter = 6
csk_depth = 1.5

boss_size_x = 8
boss_size_y = 8
boss_height = 4

# Create base plate
base = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness, centered=(True, True, False))

# Create tab on one short edge
tab = (
    cq.Workplane("XY")
    .transformed(offset=(-plate_length / 2 - tab_length / 2, 0, 0))
    .box(tab_length, tab_width, tab_thickness, centered=(True, True, False))
)
plate = base.union(tab)

# Add small through-holes at the four corners
corner_offsets = [
    (-plate_length / 2 + 10, -plate_width / 2 + 10),
    (-plate_length / 2 + 10,  plate_width / 2 - 10),
    ( plate_length / 2 - 10, -plate_width / 2 + 10),
    ( plate_length / 2 - 10,  plate_width / 2 - 10),
]
plate = (
    plate.faces(">Z")
    .workplane(offset=0)
    .pushPoints(corner_offsets)
    .hole(small_hole_diameter)
)

# Add countersunk holes
csk_offsets = [
    (-plate_length / 4, 0),
    ( plate_length / 4, 0),
    (0, -plate_width / 4),
    (0,  plate_width / 4),
]
for pt in csk_offsets:
    plate = (
        plate.faces(">Z")
        .workplane(offset=0)
        .pushPoints([pt])
        .cskHole(csk_hole_diameter, csk_diameter, csk_depth)
    )

# Add triangular cutouts
triangle_positions = [
    (-plate_length / 3, -plate_width / 4),
    (-plate_length / 3,  plate_width / 4),
    (0, -plate_width / 4),
    (0,  plate_width / 4),
    ( plate_length / 3, -plate_width / 4),
    ( plate_length / 3,  plate_width / 4),
]
for x, y in triangle_positions:
    plate = (
        plate.faces(">Z")
        .workplane(offset=0)
        .transformed(offset=(x, y, 0))
        .polyline([
            (0, triangle_side / 2),
            (-triangle_side * 0.866, -triangle_side / 4),
            ( triangle_side * 0.866, -triangle_side / 4),
        ])
        .close()
        .cutThruAll()
    )

# Add central boss
result = (
    plate.faces(">Z")
    .workplane(offset=0)
    .rect(boss_size_x, boss_size_y)
    .extrude(boss_height)
)