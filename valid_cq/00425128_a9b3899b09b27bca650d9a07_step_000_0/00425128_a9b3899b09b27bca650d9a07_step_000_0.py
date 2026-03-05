import cadquery as cq
import math

# Parametric dimensions based on visual estimation
part_length = 60.0       # Total length of the cylinder
outer_diameter = 14.0    # Outer diameter of the cylinder
hex_width = 8.0          # Width across flats (WAF) for the hex socket
socket_depth = 12.0      # Depth of the hexagonal socket

# Calculation for polygon generation:
# CadQuery defines polygons by the diameter of the circumscribed circle.
# We need to convert the "width across flats" to this diameter.
# circum_diameter = hex_width / cos(30 degrees)
hex_circum_diameter = hex_width / (math.sqrt(3) / 2)

# Generate the CAD model
result = (
    cq.Workplane("XY")
    # Base cylinder
    .circle(outer_diameter / 2.0)
    .extrude(part_length)
    # Select the top face
    .faces(">Z")
    .workplane()
    # Create hexagonal cut
    .polygon(nSides=6, diameter=hex_circum_diameter)
    .cutBlind(-socket_depth)
)