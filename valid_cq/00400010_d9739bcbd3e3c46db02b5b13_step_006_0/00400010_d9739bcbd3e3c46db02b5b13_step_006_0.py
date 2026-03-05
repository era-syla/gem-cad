import cadquery as cq
import math

# --- Model Parameters ---
# Dimensions based on a typical Metric Countersunk Screw (e.g., M12 approximation)
thread_diameter = 12.0          # Diameter of the cylindrical shaft
head_diameter = 24.0            # Outer diameter of the top of the head
total_length = 60.0             # Overall length of the screw
hex_width_across_flats = 8.0    # Size of the hex tool (Allen key)
socket_depth = 6.0              # Depth of the hex socket

# --- Derived Parameters ---
# Calculate head height assuming a standard 90-degree countersink angle.
# The side wall angle is 45 degrees relative to the vertical axis.
# Height = (Outer Radius - Inner Radius) / tan(45 degrees)
head_height = (head_diameter - thread_diameter) / 2.0
shaft_length = total_length - head_height
# Calculate the circumscribed diameter of the hexagon for the polygon function
# D_circum = (2 * width_across_flats) / sqrt(3)
hex_circum_diameter = (2.0 * hex_width_across_flats) / math.sqrt(3.0)

# --- Geometry Construction ---

# 1. Create the cylindrical shaft
result = (
    cq.Workplane("XY")
    .circle(thread_diameter / 2.0)
    .extrude(shaft_length)
)

# 2. Create the countersunk head using a loft
# We select the top face of the shaft, draw the base circle,
# offset the workplane up by the head height, draw the outer circle,
# and loft between them to create the truncated cone.
result = (
    result
    .faces(">Z").workplane()
    .circle(thread_diameter / 2.0)  # Wire 1: Base of head
    .workplane(offset=head_height)
    .circle(head_diameter / 2.0)    # Wire 2: Top of head
    .loft(combine=True)
)

# 3. Cut the hexagonal socket into the head
result = (
    result
    .faces(">Z").workplane()
    .polygon(nSides=6, diameter=hex_circum_diameter)
    .cutBlind(-socket_depth)
)