import cadquery as cq

# Angle iron / slotted angle bracket
# L-shaped cross section with oval holes along both flanges

thickness = 2.5
flange_width = 25
length = 300

# Create L-shaped profile
profile = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (flange_width, 0),
        (flange_width, thickness),
        (thickness, thickness),
        (thickness, flange_width),
        (0, flange_width),
        (0, 0)
    ])
    .close()
)

# Extrude to create the angle iron
angle_iron = profile.extrude(length)

# Add holes to the vertical flange (XZ plane - the flange along Y axis)
# Holes are oval/slotted - approximate with elongated slots
hole_spacing = 15
hole_width = 5
hole_height = 8
first_hole = 15
num_holes = int((length - first_hole) / hole_spacing)

# Cut holes in the front face (vertical flange - the one facing X direction)
# This flange lies in the YZ plane with x from 0 to thickness
# Holes centered at x = thickness/2, spaced along Z

for i in range(num_holes):
    z_pos = first_hole + i * hole_spacing
    # Hole on the flange that faces the viewer (front flange, in XZ, y=0 to flange_width)
    # Front face: y=0, hole in the face perpendicular to Y
    angle_iron = (
        angle_iron
        .faces(">Y")
        .workplane()
        .center(-(flange_width - thickness/2 - thickness), -(length/2 - z_pos))
        .slot2D(hole_height, hole_width, 90)
        .cutThruAll()
    )

# Cut holes in the side flange (the one facing Y direction, in YZ plane)
for i in range(num_holes):
    z_pos = first_hole + i * hole_spacing
    angle_iron = (
        angle_iron
        .faces(">X")
        .workplane()
        .center(-(flange_width - thickness/2 - thickness), -(length/2 - z_pos))
        .slot2D(hole_height, hole_width, 90)
        .cutThruAll()
    )

result = angle_iron