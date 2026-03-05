import cadquery as cq
import math

# Parameters based on visual estimation (Metric Button Head Screw style)
shaft_diameter = 8.0
shaft_length = 25.0
head_diameter = 14.0
head_height = 5.0
fillet_radius = 3.5  # Controls the curvature of the dome
hex_drive_af = 5.0   # Width across flats for the hex key
hex_depth = 3.0

# 1. Create the Shaft
# Start on the XY plane and extrude the main cylindrical shaft
result = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(shaft_length)

# 2. Create the Head Base
# Select the top face of the shaft and extrude the head cylinder
result = (
    result.faces(">Z")
    .workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_height)
)

# 3. Shape the Head (Dome)
# Apply a fillet to the top edge of the head to create the button profile
# We select the edge with the highest Z coordinate
result = result.edges(">Z").fillet(fillet_radius)

# 4. Create the Hex Socket (Allen Drive)
# Calculate the polygon radius (center to vertex) from the "Across Flats" dimension
# Radius = (Across Flats) / sqrt(3)
hex_radius = hex_drive_af / math.sqrt(3)

# Select the top flat face of the domed head and cut the hexagonal socket
result = (
    result.faces(">Z")
    .workplane()
    .polygon(6, hex_radius)
    .cutBlind(-hex_depth)
)