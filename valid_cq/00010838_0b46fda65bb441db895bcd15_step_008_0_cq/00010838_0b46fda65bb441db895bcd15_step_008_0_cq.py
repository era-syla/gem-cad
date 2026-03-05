import cadquery as cq

# Parametric Dimensions
base_length = 20.0
base_width = 15.0
base_height = 10.0

# Main cylindrical body dimensions
body_radius = 10.0
body_height = 25.0

# Neck dimensions (the narrower part)
neck_radius = 6.0
neck_height = 8.0

# Top cap/head dimensions
head_radius = 8.0
head_height = 5.0

# Create the rectangular base
# Using center=True for X and Y to keep it aligned with the Z-axis origin
base = cq.Workplane("XY").box(base_length, base_width, base_height, centered=(True, True, False))

# Create the main cylindrical body on top of the base
# We select the top face of the base, work on it, and extrude
body = (
    base.faces(">Z")
    .workplane()
    .circle(body_radius)
    .extrude(body_height)
)

# Create the neck on top of the main body
neck = (
    body.faces(">Z")
    .workplane()
    .circle(neck_radius)
    .extrude(neck_height)
)

# Create the top head/cap on top of the neck
head = (
    neck.faces(">Z")
    .workplane()
    .circle(head_radius)
    .extrude(head_height)
)

# The variable 'result' contains the final geometry
result = head