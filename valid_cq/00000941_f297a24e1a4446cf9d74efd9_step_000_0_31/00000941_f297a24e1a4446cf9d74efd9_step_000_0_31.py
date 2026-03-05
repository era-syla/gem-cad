import cadquery as cq

# Parametric dimensions
plate_width = 40.0
plate_height = 40.0
plate_thickness = 5.0

hole1_diameter = 6.0
hole2_diameter = 14.0
hole1_x_offset = -11.0
hole2_x_offset = 9.0
hole_y_offset = 10.0

rod_diameter = 8.0
rod_length = 100.0

disk_diameter = 36.0
disk_thickness_1 = 2.0
disk_groove_diameter = 34.5
disk_groove_thickness = 0.5
disk_thickness_2 = 2.0

center_indent_diameter = 8.0
center_indent_depth = 1.0

# 1. Base Plate
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Holes in the base plate
result = (
    result.faces(">Z").workplane()
    .pushPoints([(hole1_x_offset, hole_y_offset)])
    .circle(hole1_diameter / 2.0)
    .pushPoints([(hole2_x_offset, hole_y_offset)])
    .circle(hole2_diameter / 2.0)
    .cutThruAll()
)

# 3. Main extending rod
result = (
    result.faces(">Z").workplane()
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
)

# 4. End disk - inner section
result = (
    result.faces(">Z").workplane()
    .circle(disk_diameter / 2.0)
    .extrude(disk_thickness_1)
)

# 5. End disk - shallow groove
result = (
    result.faces(">Z").workplane()
    .circle(disk_groove_diameter / 2.0)
    .extrude(disk_groove_thickness)
)

# 6. End disk - outer section
result = (
    result.faces(">Z").workplane()
    .circle(disk_diameter / 2.0)
    .extrude(disk_thickness_2)
)

# 7. Center indent on the front face of the disk
result = (
    result.faces(">Z").workplane()
    .circle(center_indent_diameter / 2.0)
    .cutBlind(-center_indent_depth)
)