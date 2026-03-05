import cadquery as cq
import math

# --- Parametric Dimensions (Standard M6-style proportions) ---
head_diameter = 10.0
head_height = 6.0
shank_diameter = 6.0
shank_length = 24.0
socket_size = 5.0       # Hex key size (across flats)
socket_depth = 3.5
head_chamfer = 0.5
tip_chamfer = 0.5

# Calculate the circumscribed diameter of the hexagon for the polygon function
# Relation: Diameter = (Across Flats) / cos(30 degrees)
socket_outer_diam = socket_size / math.cos(math.radians(30))

# --- 3D Modeling ---

# 1. Create the cylindrical head
result = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(head_height)

# 2. Apply chamfer to the top edge of the head
result = result.edges(">Z").chamfer(head_chamfer)

# 3. Create the shank extending from the bottom of the head
# We select the bottom face ("<Z") and extrude. 
# Note: Extruding from a bottom face usually follows the normal (downwards).
result = (
    result.faces("<Z")
    .workplane()
    .circle(shank_diameter / 2.0)
    .extrude(shank_length)
)

# 4. Apply chamfer to the tip of the shank (the new lowest edge)
result = result.edges("<Z").chamfer(tip_chamfer)

# 5. Cut the hexagonal socket into the top of the head
# We select the top face (">Z") and cut blind in the negative direction (into the part)
result = (
    result.faces(">Z")
    .workplane()
    .polygon(6, socket_outer_diam)
    .cutBlind(-socket_depth)
)