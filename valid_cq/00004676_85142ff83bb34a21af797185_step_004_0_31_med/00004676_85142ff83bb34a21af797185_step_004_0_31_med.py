import cadquery as cq
import math

# Parameters for an M5-like socket head cap screw
shaft_diameter = 5.0
shaft_length = 35.0
head_diameter = 8.5
head_height = 5.0
hex_across_flats = 4.0
hex_depth = 3.0
head_chamfer = 0.4
shaft_chamfer = 0.5

# Calculate the circumscribed diameter for the hex socket
hex_circum_diameter = hex_across_flats / math.cos(math.radians(30))

# Create the main body (shaft and head)
result = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2.0)
    .extrude(-shaft_length)
    .faces(">Z")
    .workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_height)
)

# Apply chamfers to the top of the head and bottom of the shaft
result = (
    result
    .edges(">Z").chamfer(head_chamfer)
    .edges("<Z").chamfer(shaft_chamfer)
)

# Cut the hexagonal socket into the top of the head
result = (
    result
    .faces(">Z")
    .workplane()
    .polygon(6, hex_circum_diameter)
    .cutBlind(-hex_depth)
)