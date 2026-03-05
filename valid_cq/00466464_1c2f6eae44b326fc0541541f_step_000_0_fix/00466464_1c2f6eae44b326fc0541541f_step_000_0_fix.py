import cadquery as cq

# Parameters
wall = 2
floor_thickness = 3
height = 15
length_body = 60
width_body = 60
length_ext = 40
bar_width = 4
gap = 3
hole_dia = 5
fillet_r = 1

bars_total = 2*bar_width + gap

# Create the bottom floor
floor = cq.Workplane("XY").box(length_body, width_body, floor_thickness, centered=(True,True,False))

# Create the walls
walls = (
    cq.Workplane("XY")
    .workplane(offset=floor_thickness)
    .rect(length_body, width_body)
    .rect(length_body-2*wall, width_body-2*wall)
    .extrude(height - floor_thickness)
)

# Combine floor and walls
body = floor.union(walls)

# Create the handle plate
handle_plate = (
    cq.Workplane("XY")
    .workplane(offset=floor_thickness)
    .transformed(offset=(length_body/2 + length_ext/2, 0, 0))
    .rect(length_ext, bars_total)
    .extrude(height - floor_thickness)
)

part = body.union(handle_plate)

# Cut the slot between the two prongs
slot = (
    cq.Workplane("XY")
    .transformed(offset=(length_body/2 + length_ext/2, 0, floor_thickness))
    .box(length_ext, gap, height - floor_thickness, centered=(True,True,False))
)
part = part.cut(slot)

# Cut the cylindrical hole through the prongs
hole = (
    cq.Workplane("XZ")
    .transformed(
        offset=(
            length_body/2 + length_ext - bar_width,
            -bars_total/2,
            floor_thickness + (height - floor_thickness)/2
        )
    )
    .circle(hole_dia/2)
    .extrude(bars_total)
)
part = part.cut(hole)

# Fillet vertical edges
part = part.edges("|Z").fillet(fillet_r)

result = part