import cadquery as cq

# Define basic parameters
shaft_diameter = 5
shaft_length = 40
head_diameter = 10
head_height = 3
hex_socket_diameter = 3

# Create the shaft
shaft = cq.Workplane("XY").circle(shaft_diameter / 2).extrude(shaft_length)

# Create the head
head = cq.Workplane("XY").circle(head_diameter / 2).extrude(head_height)

# Combine shaft and head
bolt = shaft.union(head.translate((0, 0, shaft_length)))

# Create the hex socket
hex_socket = cq.Workplane("XY").polygon(6, hex_socket_diameter).extrude(head_height)

# Cut the hex socket
result = bolt.cut(hex_socket.translate((0, 0, shaft_length)))