import cadquery as cq

# Socket head cap screw
# Parameters
head_diameter = 10.0
head_height = 10.0
shaft_diameter = 6.0
shaft_length = 35.0
hex_size = 5.0  # hex socket across flats
hex_depth = 5.0

# Create the shaft
shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# Create the head (cylinder sitting on top of shaft)
head = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .circle(head_diameter / 2)
    .extrude(head_height)
)

# Combine shaft and head
body = shaft.union(head)

# Add fillet at the top edge of the head
body = (
    body
    .faces(">Z")
    .edges()
    .chamfer(0.5)
)

# Add fillet where shaft meets head (bottom of head)
# We'll add a small fillet at the base of the head
body = (
    body
    .faces(">Z[-2]")
    .edges("%Circle")
    .fillet(0.8)
)

# Cut hex socket into the top of the head
hex_socket = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length + head_height)
    .polygon(6, hex_size)
    .extrude(hex_depth)
)

result = body.cut(hex_socket)