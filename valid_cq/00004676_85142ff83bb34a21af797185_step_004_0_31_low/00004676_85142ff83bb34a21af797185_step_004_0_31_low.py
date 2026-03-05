import cadquery as cq

# Parameters for an M5 socket head cap screw
head_diameter = 8.5
head_height = 5.0
shaft_diameter = 5.0
shaft_length = 30.0
hex_key_size = 4.0
hex_depth = 2.5
chamfer_size = 0.5

# Create the shaft
result = cq.Workplane("XY").circle(shaft_diameter / 2).extrude(-shaft_length)

# Create the head
head = (
    cq.Workplane("XY")
    .circle(head_diameter / 2)
    .extrude(head_height)
    .faces(">Z")
    .polygon(6, hex_key_size * 2 / (3**0.5))  # Circumscribed circle diameter for hex
    .cutBlind(-hex_depth)
)

# Combine head and shaft
result = result.union(head)

# Chamfer the top edge of the head and the bottom edge of the shaft
result = result.edges(">Z").chamfer(chamfer_size)
result = result.edges("<Z").chamfer(chamfer_size)