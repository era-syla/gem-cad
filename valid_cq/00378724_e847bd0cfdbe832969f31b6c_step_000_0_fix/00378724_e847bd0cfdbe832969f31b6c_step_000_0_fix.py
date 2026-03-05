import cadquery as cq

# Parameters
plate_length = 80
plate_width = 20
plate_thickness = 10
clamp_radius = 20
clamp_center_x = plate_length/2 - clamp_radius

# Base plate
plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Cylindrical clamp extension
clamp = (
    cq.Workplane("XY")
    .transformed(offset=(clamp_center_x, 0, 0))
    .circle(clamp_radius)
    .extrude(plate_thickness)
)

# Combine plate and clamp
result = plate.union(clamp)

# Cut the opening in the clamp (make it C-shaped)
gap = (
    cq.Workplane("XY")
    .box(clamp_radius, plate_width, plate_thickness)
    .translate((clamp_center_x + clamp_radius/2, 0, plate_thickness/2))
)
result = result.cut(gap)

# Top holes (through the plate)
top_hole_positions = [(-15, 0), (15, 0)]
result = result.faces(">Z").workplane().pushPoints(top_hole_positions).hole(6)

# Side holes through the cylindrical clamp (along X axis)
side_hole_radius = 2.5
side_offsets = [plate_width/2 - 2, -(plate_width/2 - 2)]
for y_off in side_offsets:
    cut_hole = (
        cq.Workplane("YZ")
        .transformed(offset=(clamp_center_x, y_off, plate_thickness/2))
        .circle(side_hole_radius)
        .extrude(plate_length)
    )
    result = result.cut(cut_hole)

# Hole through the left extension block (along Y axis)
left_hole_x = -plate_length/2 + 10
cut_left = (
    cq.Workplane("XZ")
    .transformed(offset=(left_hole_x, -plate_width/2, plate_thickness/2))
    .circle(2.5)
    .extrude(plate_width)
)
result = result.cut(cut_left)