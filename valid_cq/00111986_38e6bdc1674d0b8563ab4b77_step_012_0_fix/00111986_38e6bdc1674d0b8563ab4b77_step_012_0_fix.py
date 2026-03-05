import cadquery as cq

# Parameters
thickness = 3.0
plate_width = 40.0
plate_height = 72.0
hole_diameter = 6.0
cols = 4
rows = 6
pitch_x = 10.0
pitch_y = 12.0
tab_depth = 5.0
tab_height = 8.0

# Plain flange
plate1 = cq.Workplane("XY").box(plate_width, thickness, plate_height)

# Holed flange
plate2 = (
    cq.Workplane("XY")
    .transformed(offset=(plate_width/2 + thickness/2, 0, 0))
    .box(thickness, plate_width, plate_height)
)
# Drill grid of holes through plate2
points = [
    ((i - (cols - 1) / 2) * pitch_x, (j - (rows - 1) / 2) * pitch_y)
    for i in range(cols)
    for j in range(rows)
]
plate2 = plate2.faces(">X").workplane().pushPoints(points).hole(hole_diameter)

# Top tab on holed flange
tab = (
    cq.Workplane("XY")
    .transformed(
        offset=(
            plate_width / 2 + thickness + tab_depth / 2,
            0,
            plate_height / 2 + tab_height / 2,
        )
    )
    .box(tab_depth, plate_width, tab_height)
)

# Combine all parts
result = plate1.union(plate2).union(tab)