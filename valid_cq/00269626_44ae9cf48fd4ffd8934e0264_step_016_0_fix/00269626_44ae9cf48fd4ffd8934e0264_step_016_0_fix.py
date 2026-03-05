import cadquery as cq

rod_length = 200
rod_d = 4
spacing = rod_d * 2
positions = [(-spacing, 0), (0, 0), (spacing, 0)]

rods = None
for x, y in positions:
    cyl = cq.Workplane("XY") \
        .transformed(offset=(x, y, 0)) \
        .circle(rod_d / 2) \
        .extrude(rod_length)
    rods = cyl if rods is None else rods.union(cyl)

plate_t = 4
plate_x = 2 * spacing + rod_d + 4
plate_y = rod_d + 4

plate1 = cq.Workplane("XY").box(plate_x, plate_y, plate_t)
plate2 = cq.Workplane("XY") \
    .transformed(offset=(0, 0, rod_length - plate_t)) \
    .box(plate_x, plate_y, plate_t)

result = rods.union(plate1).union(plate2)