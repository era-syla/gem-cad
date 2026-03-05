import cadquery as cq

# Dimensions
plate_width = 10
plate_height = 70
plate_thickness = 3

hole_diameter = 4.5
countersink_diameter = 7
hole_spacing = 10
num_holes = 6

notch_width = 3
notch_depth = 2

# Create the base plate
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
)

# Add chamfers to the top and bottom ends (the angled corners visible in image)
result = (
    result
    .edges("|Z")
    .edges(cq.NearestToPointSelector((0, plate_height/2, 0)))
    .chamfer(1.5)
)

# Restart with a cleaner approach
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# Chamfer the long vertical edges
result = result.edges("|Z").chamfer(1.0)

# Add holes with countersinks
hole_positions = []
for i in range(num_holes):
    y_pos = -(num_holes - 1) * hole_spacing / 2 + i * hole_spacing
    hole_positions.append((0, y_pos))

# Drill through holes
for pos in hole_positions:
    result = (
        result
        .faces(">Z")
        .workplane()
        .center(pos[0], pos[1])
        .circle(hole_diameter / 2)
        .cutThruAll()
    )

# Add countersinks on top face
for pos in hole_positions:
    result = (
        result
        .faces(">Z")
        .workplane()
        .center(pos[0], pos[1])
        .circle(countersink_diameter / 2)
        .cutBlind(-1.0)
    )

# Add side notches (the indentations on the sides between holes)
# Notches on the left and right sides between holes
notch_positions = []
for i in range(num_holes - 1):
    y_pos = -(num_holes - 1) * hole_spacing / 2 + i * hole_spacing + hole_spacing / 2
    notch_positions.append(y_pos)

# Cut notches from left side
for y_pos in notch_positions:
    result = (
        result
        .faces("<X")
        .workplane()
        .center(y_pos, 0)
        .rect(notch_width, plate_thickness + 1)
        .cutBlind(-notch_depth)
    )

# Cut notches from right side
for y_pos in notch_positions:
    result = (
        result
        .faces(">X")
        .workplane()
        .center(-y_pos, 0)
        .rect(notch_width, plate_thickness + 1)
        .cutBlind(-notch_depth)
    )