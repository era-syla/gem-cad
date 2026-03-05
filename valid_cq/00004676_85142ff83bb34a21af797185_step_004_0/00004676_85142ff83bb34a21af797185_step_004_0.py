import cadquery as cq
import math

# --- Parameters ---
# Dimensions based on a standard Metric Socket Head Cap Screw (approx M5x40)
shaft_diameter = 5.0
shaft_length = 40.0
head_diameter = 8.5
head_height = 5.0
hex_flat_size = 4.0      # Distance across flats (Allen key size)
socket_depth = 3.0       # Depth of the hexagonal socket
tip_chamfer = 0.5        # Chamfer at the threaded tip
head_chamfer = 0.3       # Cosmetic chamfer on the top edge of the head

# --- 3D Modeling ---

# 1. Create the main Shaft
# Start on the XY plane and extrude the shaft length along Z
result = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(shaft_length)

# 2. Create the Head
# Select the top face of the shaft and extrude the larger head diameter
result = (
    result.faces(">Z")
    .workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_height)
)

# 3. Create the Hex Socket
# Calculate the circumscribed diameter (corner-to-corner) for the hexagon
# Formula: Diameter = 2 * (Size_across_flats / sqrt(3))
hex_circum_diameter = 2 * hex_flat_size / math.sqrt(3)

# Cut the hexagon into the top face
result = (
    result.faces(">Z")
    .workplane()
    .polygon(nSides=6, diameter=hex_circum_diameter)
    .cutBlind(-socket_depth)
)

# 4. Finishing Details
# Chamfer the bottom tip of the shaft (insertion aid)
result = result.edges("<Z").chamfer(tip_chamfer)

# Chamfer the top outer edge of the head
# Use a filter to select only the circular outer edge, ignoring the hexagonal edges
result = (
    result.faces(">Z")
    .edges()
    .filter(lambda e: e.geomType() == "CIRCLE")
    .chamfer(head_chamfer)
)