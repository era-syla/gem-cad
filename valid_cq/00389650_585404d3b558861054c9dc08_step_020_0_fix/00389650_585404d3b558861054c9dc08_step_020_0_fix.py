import cadquery as cq

# Parameters
plate_length = 60.0
plate_width = 40.0
plate_thickness = 6.0
wall_thickness = 4.0
wall_height = 20.0
central_hole_dia = 20.0
mount_hole_dia = 4.0
side_hole_dia = 4.0
mount_offset_x = plate_length/2 - 10.0
mount_offset_y = plate_width/2 - 10.0

# Base plate
plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Back wall (at +Y edge)
back_wall = (
    cq.Workplane("XY")
      .workplane(offset=plate_thickness/2)
      .center(0, plate_width/2 - wall_thickness/2)
      .rect(plate_length, wall_thickness)
      .extrude(-wall_height)
)

# Left wall (at -X edge)
left_wall = (
    cq.Workplane("XY")
      .workplane(offset=plate_thickness/2)
      .center(-plate_length/2 + wall_thickness/2, 0)
      .rect(wall_thickness, plate_width)
      .extrude(-wall_height)
)

# Combine plate and walls
base = plate.union(back_wall).union(left_wall)

# Drill central hole through plate
result = base.faces(">Z").workplane().hole(central_hole_dia)

# Drill four mounting holes through plate
mount_points = [
    ( mount_offset_x,  mount_offset_y),
    (-mount_offset_x,  mount_offset_y),
    (-mount_offset_x, -mount_offset_y),
    ( mount_offset_x, -mount_offset_y),
]
for x, y in mount_points:
    result = result.faces(">Z").workplane().center(x, y).hole(mount_hole_dia)

# Drill hole through left wall
left_hole_center_x = -plate_length/2 + wall_thickness/2
left_hole_center_z = plate_thickness/2 - wall_height/2
result = result.cut(
    cq.Workplane("YZ", origin=(left_hole_center_x, 0, left_hole_center_z))
      .circle(side_hole_dia/2)
      .extrude(wall_thickness + 1)
)

# Drill hole through back wall
back_hole_center_y = plate_width/2 - wall_thickness/2
back_hole_center_z = plate_thickness/2 - wall_height/2
result = result.cut(
    cq.Workplane("XZ", origin=(0, back_hole_center_y, back_hole_center_z))
      .circle(side_hole_dia/2)
      .extrude(wall_thickness + 1)
)