import cadquery as cq

# Parameters
plate_x = 120
plate_y = 70
plate_th = 6

# Create base plate
plate = cq.Workplane("XY").box(plate_x, plate_y, plate_th)

# Drill hole pattern (3 clusters of 4 holes)
hole_d = 4
cluster_x = [-40, 0, 40]
points = []
for cx in cluster_x:
    for dx in (-10, 10):
        for dy in (-10, 10):
            points.append((cx + dx, dy))
plate = plate.faces(">Z").workplane().pushPoints(points).hole(hole_d)

# Bracket parameters
br_base_l = 20
br_base_w = 15
br_base_th = 4
wall_th = 3
wall_h = 10

# Create bracket base
bracket_base = (
    cq.Workplane("XY")
    .transformed(offset=(-20, 0, plate_th/2 + br_base_th/2))
    .box(br_base_l, br_base_w, br_base_th)
)

# Create bracket walls
wall1 = (
    cq.Workplane("XY")
    .transformed(
        offset=(
            -20,
            br_base_w/2 - wall_th/2,
            plate_th + br_base_th + wall_h/2
        )
    )
    .box(br_base_l, wall_th, wall_h)
)
wall2 = (
    cq.Workplane("XY")
    .transformed(
        offset=(
            -20,
            -(br_base_w/2 - wall_th/2),
            plate_th + br_base_th + wall_h/2
        )
    )
    .box(br_base_l, wall_th, wall_h)
)

# Create through-hole in bracket
cyl = (
    cq.Workplane("XY")
    .transformed(offset=(-20, 0, plate_th/2))
    .cylinder(plate_th + br_base_th + wall_h, 6)
)

# Connector parameters
con_base_l = 20
con_base_w = 15
con_base_th = 4
pin_l = 3
pin_w = 3
pin_h = 10
pin_offsets = [-5, 0, 5]

# Create connector base
con_base = (
    cq.Workplane("XY")
    .transformed(offset=(20, 0, plate_th/2 + con_base_th/2))
    .box(con_base_l, con_base_w, con_base_th)
)

# Create pins
pin1 = (
    cq.Workplane("XY")
    .transformed(offset=(20 + pin_offsets[0], 0, plate_th + con_base_th + pin_h/2))
    .box(pin_l, pin_w, pin_h)
)
pin2 = (
    cq.Workplane("XY")
    .transformed(offset=(20 + pin_offsets[1], 0, plate_th + con_base_th + pin_h/2))
    .box(pin_l, pin_w, pin_h)
)
pin3 = (
    cq.Workplane("XY")
    .transformed(offset=(20 + pin_offsets[2], 0, plate_th + con_base_th + pin_h/2))
    .box(pin_l, pin_w, pin_h)
)

# Combine all and subtract bracket hole
result = (
    plate
    .union(bracket_base)
    .union(wall1)
    .union(wall2)
    .union(con_base)
    .union(pin1)
    .union(pin2)
    .union(pin3)
    .cut(cyl)
)