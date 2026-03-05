import cadquery as cq

# Parameters
length = 300
width = 100
plate_thickness = 5
flange_length = 80
wall_height = 30
wall_thickness = 3
n_holes = 10
hole_diameter = 4
margin_x = 15
slot_length = 60
slot_width = 6
slot_offset = 20

# Base plate (channel bottom)
base = cq.Workplane("XY").box(length, width, plate_thickness)

# Flange plate at one end
flange = (
    cq.Workplane("XY")
    .box(flange_length, width, plate_thickness)
    .translate((length/2 + flange_length/2, 0, plate_thickness/2))
)

# Side walls (only under the main channel, not under the flange)
left_wall = (
    cq.Workplane("XY")
    .box(length, wall_thickness, wall_height)
    .translate((0, -width/2 + wall_thickness/2, plate_thickness + wall_height/2))
)
right_wall = (
    cq.Workplane("XY")
    .box(length, wall_thickness, wall_height)
    .translate((0, width/2 - wall_thickness/2, plate_thickness + wall_height/2))
)

# Combine all channel bodies
result = base.union(flange).union(left_wall).union(right_wall)

# Prepare hole positions along the channel length
xs = [
    -length/2 + margin_x + i * ((length - 2 * margin_x) / (n_holes - 1))
    for i in range(n_holes)
]

# Drill holes through both side walls
result = (
    result.faces("<Y")
    .workplane()
    .pushPoints([(x, 0) for x in xs])
    .hole(hole_diameter)
)
result = (
    result.faces(">Y")
    .workplane()
    .pushPoints([(x, 0) for x in xs])
    .hole(hole_diameter)
)

# Cut rectangular slots in the flange top plate
slot_centers = [
    (length/2 + flange_length/2,  slot_offset),
    (length/2 + flange_length/2, -slot_offset),
]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(slot_centers)
    .rect(slot_length, slot_width)
    .cutThruAll()
)