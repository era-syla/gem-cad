import cadquery as cq

# Geometric Parameters
flange_width = 160.0
flange_height = 100.0
flange_thickness = 10.0

body_width = 90.0
body_height = 70.0
body_length = 120.0

hole_diameter = 5.0
hole_margin_side = 12.0
hole_spacing_vert = 30.0

# 1. Create the front Flange plate
# Oriented in the XY plane, centered at origin
result = cq.Workplane("XY").box(flange_width, flange_height, flange_thickness)

# 2. Create the Body block attached to the back
# Select the back face (negative Z direction) of the flange
# Create a workplane, draw the body profile, and extrude
result = (
    result.faces("<Z")
    .workplane()
    .rect(body_width, body_height)
    .extrude(body_length)
)

# 3. Create the bolt holes
# Calculate horizontal position relative to center
x_pos = (flange_width / 2.0) - hole_margin_side

# Define the list of hole centers (x, y)
# 3 holes on the left, 3 holes on the right
hole_points = [
    (-x_pos, 0),
    (-x_pos, hole_spacing_vert),
    (-x_pos, -hole_spacing_vert),
    (x_pos, 0),
    (x_pos, hole_spacing_vert),
    (x_pos, -hole_spacing_vert),
]

# Cut the holes through the flange
# Select the front face (positive Z), push points, and cut
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)