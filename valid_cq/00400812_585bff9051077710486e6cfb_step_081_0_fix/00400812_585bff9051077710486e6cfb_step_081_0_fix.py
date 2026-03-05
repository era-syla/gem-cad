import cadquery as cq

# Parameters
thickness = 5.0
width = 200.0
height = 150.0
margin_x = width/2 - 8.0
margin_y = height/2 - 8.0
notch_radius = 20.0
hole_radius = 1.5

# Start with base plate
plate = cq.Workplane("XY").rect(width, height).extrude(thickness)

# Cut semicircular notches on left and right edges
plate = (
    plate
    .faces(">Z")
    .workplane()
    .pushPoints([( margin_x, 0), (-margin_x, 0)])
    .circle(notch_radius)
    .cutBlind(-thickness)
)

# Define hole positions
hole_positions = []

# Corner holes
for x in (-margin_x, margin_x):
    for y in (-margin_y, margin_y):
        hole_positions.append((x, y))

# Holes above notches
hole_positions.append(( margin_x,  20.0))
hole_positions.append((-margin_x,  20.0))

# Center hole
hole_positions.append((0.0, 0.0))

# Bottom-left small cluster (2 holes)
hole_positions.append((-70.0, -45.0))
hole_positions.append((-50.0, -45.0))

# Bottom-right cluster (4 holes)
for dx in (-5.0, 5.0):
    for dy in (-5.0, -5.0):
        hole_positions.append((70.0 + dx, -45.0 + dy))

# Drill all holes through the plate
plate = (
    plate
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(hole_radius)
    .cutThruAll()
)

result = plate