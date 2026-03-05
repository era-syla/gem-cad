import cadquery as cq

# Parameters for the Socket Head Cap Screw
# Based on approximate standard ISO 4762 dimensions for something like an M5 or M6 screw
shaft_diameter = 5.0      # M5
shaft_length = 40.0       # Length of the shaft under the head
head_diameter = 8.5       # Diameter of the screw head
head_height = 5.0         # Height of the screw head
hex_socket_size = 4.0     # Size of the hex key (across flats)
hex_socket_depth = 3.0    # Depth of the hex socket

# Create the screw
# 1. Create the shaft
shaft = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(shaft_length)

# 2. Create the head
# We start drawing on the top face of the shaft
head = (
    shaft.faces(">Z")
    .workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_height)
)

# 3. Cut the hex socket
# We select the very top face of the newly created head
result = (
    head.faces(">Z")
    .workplane()
    .polygon(nSides=6, diameter=hex_socket_size / 0.866025) # 0.866 is cos(30), converting flat-to-flat to diameter
    .cutBlind(-hex_socket_depth)
)

# Optional: Add a small chamfer to the bottom of the shaft for realism
result = result.edges("<Z").chamfer(0.5)

# Optional: Add a small fillet under the head for stress relief/realism
# We select the edge where the shaft meets the head
result = result.edges(cq.selectors.RadiusNthSelector(1)).fillet(0.2)

# Export or display
# show_object(result)