import cadquery as cq

# Parameters
block_thick = 30
block_depth = 30
block_height = 100
wall = 3
inner_radius = block_height/2 - wall
cav_extra = 5

# Main block with curved interior cutout
block = cq.Workplane("XY").box(block_thick, block_depth, block_height)
cavity = (
    cq.Workplane("XZ")
    .transformed(offset=(block_thick/2 - wall, -block_depth/2 - cav_extra, 0))
    .circle(inner_radius)
    .extrude(block_depth + 2*cav_extra)
)
body = block.cut(cavity)

# Plate arm
plate_len = 120
plate_width = 15
plate_thick = 3
plate = (
    cq.Workplane("XY")
    .box(plate_len, plate_width, plate_thick)
    .translate((-block_thick/2 - plate_len/2, 0, 0))
)

# Drill holes in the end tab of the plate
hole_offset_x = -block_thick/2 - plate_len + 10
hole_ys = [5, -5]
plate = (
    plate.faces(">Z")
    .workplane()
    .pushPoints([(hole_offset_x, y) for y in hole_ys])
    .hole(4)
)

# Combine block and plate
result = body.union(plate)