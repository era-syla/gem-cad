import cadquery as cq

# Parameters
thickness = 10
base_length = 80
base_width = thickness
base_thickness = thickness
plate_height = 50
gusset_height = 30
side_hole_dia = 10
gusset_hole_dia = 8

# Base
base = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# Side plate template with hole through its thickness (Y direction)
side_plate = (
    cq.Workplane("XY")
    .box(thickness, base_width, plate_height)
    .faces(">Y")
    .workplane()
    .hole(side_hole_dia)
)

# Position left and right plates
plate_z = base_thickness / 2 + plate_height / 2
x_pos = base_length / 2 - thickness / 2
left_plate = side_plate.translate((-x_pos, 0, plate_z))
right_plate = side_plate.translate(( x_pos, 0, plate_z))

# Gusset as triangular plate between the side plates
inner_width = base_length - 2 * thickness
pts = [
    (-inner_width / 2, base_thickness),
    ( inner_width / 2, base_thickness),
    (             0, base_thickness + gusset_height),
]
gusset = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(base_width)
)

# Hole in the gusset (centered at its centroid)
# Face(">Y") is the front face of the gusset; its bounding-box center in Z is base_thickness + gusset_height/2
# We offset by -gusset_height/6 to reach centroid at base_thickness + gusset_height/3
gusset = (
    gusset.faces(">Y")
    .workplane()
    .pushPoints([(0, -gusset_height / 6)])
    .hole(gusset_hole_dia)
)

# Combine all parts
result = base.union(left_plate).union(right_plate).union(gusset)