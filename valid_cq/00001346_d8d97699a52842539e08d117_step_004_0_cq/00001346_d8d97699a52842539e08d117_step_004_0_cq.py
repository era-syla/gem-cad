import cadquery as cq

# Parametric dimensions for a standard-looking Socket Head Cap Screw
# Modeled loosely after an M6 or M8 screw geometry
head_diameter = 16.0
head_height = 8.0
shank_diameter = 10.0
shank_length = 15.0  # Length of the unthreaded/body portion visible
hex_socket_size = 6.0 # Distance across flats for the hex key
hex_socket_depth = 4.0
chamfer_size = 0.5   # Chamfer on the top edge of the head
bottom_chamfer = 0.5 # Chamfer at the bottom of the shank

# Create the base shape (Shank)
shank = cq.Workplane("XY").circle(shank_diameter / 2.0).extrude(shank_length)

# Create the Head
# We extrude from the top face of the shank
head = (
    shank.faces(">Z")
    .workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_height)
)

# Create the Hex Socket
# We cut into the top face of the head
# polygon(6, ...) creates a hexagon. The diameter argument in CadQuery for polygons
# corresponds to the circumscribed circle diameter.
# To convert flat-to-flat distance (s) to circumscribed diameter (d): d = s / cos(30) = s * 2 / sqrt(3)
import math
circumscribed_diameter = hex_socket_size * 2 / math.sqrt(3)

result = (
    head.faces(">Z")
    .workplane()
    .polygon(6, circumscribed_diameter)
    .cutBlind(-hex_socket_depth)
)

# Apply finishing touches (Chamfers)

# 1. Chamfer the top outer edge of the head
result = result.edges(">Z").chamfer(chamfer_size)

# 2. Chamfer the bottom edge of the shank
result = result.edges("<Z").chamfer(bottom_chamfer)

# Note: Threads are typically computationally expensive and complex to model 
# and are often omitted in CAD representations unless strictly necessary. 
# This model represents the "envelope" geometry as seen in the image.