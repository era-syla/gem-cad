import cadquery as cq

# Parameters
length = 100.0
width = 30.0
height = 20.0
wall_thickness = 4.0
floor_thickness = 3.0

# Create side‐profile in the X‐Z plane
profile = [
    (0, 0),
    (length, 0),
    (length, height),
    (length - wall_thickness, height),
    (length - wall_thickness, floor_thickness),
    (wall_thickness, floor_thickness),
    (wall_thickness, height),
    (0, height),
]

# Extrude the profile along Y to create the main bracket shape
result = (
    cq.Workplane("XZ")
    .polyline(profile)
    .close()
    .extrude(width)
)

# Front‐end notch cutout in the side walls
slot_depth = wall_thickness
slot_height = height * 0.5
result = (
    result
    .faces("<X")
    .workplane(centerOption="CenterOfBoundBox")
    .rect(slot_depth, width)
    .cutBlind(slot_height)
)

# Back‐end pocket cutout
pocket_depth = wall_thickness * 1.5
pocket_height = height * 0.7
result = (
    result
    .faces(">X")
    .workplane(centerOption="CenterOfBoundBox")
    .rect(pocket_depth, width)
    .cutBlind(pocket_height)
)