import cadquery as cq

# Parameters
length = 100.0
width = 30.0
thickness = 5.0

center_length = 30.0
notch_length = 20.0
notch_depth = 6.0

hole_spacing = 15.0
hole_diameter = 5.0
chamfer_size = 3.0

# Calculate notch positions
cx = center_length / 2.0 + notch_length / 2.0
cy = width / 2.0

# Create base geometry and cut side notches
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (cx, cy),
        (cx, -cy),
        (-cx, cy),
        (-cx, -cy)
    ])
    .rect(notch_length, notch_depth * 2)
    .cutThruAll()
)

# Apply chamfer to the top edges at the extreme ends
result = result.edges("(>X or <X) and >Z").chamfer(chamfer_size)

# Add the central holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (hole_spacing / 2.0, 0),
        (-hole_spacing / 2.0, 0)
    ])
    .hole(hole_diameter)
)