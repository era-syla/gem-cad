import cadquery as cq

# Parameters
bar_length = 200
bar_width = 2
bar_height = 2

plate_length = 5
plate_width = 3
plate_height = 2

cyl_dia = 2
cyl_height = 2

cyl_x_offset = -20
plate_x_offset = 0

# Create main bar
bar = cq.Workplane("XY").box(bar_length, bar_width, bar_height)

# Create rectangular plate on top of the bar
plate = (
    cq.Workplane("XY")
    .transformed(offset=(plate_x_offset, 0, bar_height/2 + plate_height/2))
    .box(plate_length, plate_width, plate_height)
)

# Create cylindrical peg on top of the bar
cylinder = (
    cq.Workplane("XY")
    .transformed(offset=(cyl_x_offset, 0, bar_height/2 + cyl_height/2))
    .circle(cyl_dia / 2)
    .extrude(cyl_height)
)

result = bar.union(plate).union(cylinder)