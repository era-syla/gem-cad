import cadquery as cq

# Socket head cap screw
# Parameters
head_diameter = 10.0
head_height = 6.0
shaft_diameter = 6.0
shaft_length = 28.0
hex_socket_diameter = 5.0  # across flats (inscribed circle diameter)
hex_depth = 3.5

# Create the head (cylinder)
head = (
    cq.Workplane("XY")
    .circle(head_diameter / 2)
    .extrude(head_height)
)

# Create the shaft (cylinder extending downward from bottom of head)
shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2)
    .extrude(-shaft_length)
)

# Combine head and shaft
result = head.union(shaft)

# Add chamfer at bottom of shaft
result = (
    result
    .faces("<Z")
    .edges()
    .chamfer(0.5)
)

# Add fillet at junction between head and shaft (bottom edge of head on outside)
# We'll add a small fillet on the top edge of the head
result = (
    result
    .faces(">Z")
    .edges()
    .fillet(0.5)
)

# Cut hex socket into the top of the head
# Hex socket: polygon inscribed in circle of hex_socket_diameter/2
# For a hex key, diameter across flats = hex_socket_diameter
# across corners = hex_socket_diameter / cos(30deg)
hex_across_corners = (hex_socket_diameter / 2) / (3**0.5 / 2) * 2  # diameter across corners

result = (
    result
    .faces(">Z")
    .workplane()
    .polygon(6, hex_across_corners)
    .cutBlind(-hex_depth)
)