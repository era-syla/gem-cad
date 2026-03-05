import cadquery as cq
import math

# --- Parametric Dimensions ---
# Dimensions are estimated based on visual proportions
shank_diameter = 8.0
shank_length = 45.0
neck_diameter = 4.8
neck_length = 12.0
head_diameter = 9.0
head_height = 7.0

# Feature Details
bottom_chamfer_size = 0.5
shoulder_chamfer_size = 0.5  # Transition from shank to neck
head_top_fillet = 1.0
neck_head_fillet = 0.4
hex_socket_size = 4.0        # Flat-to-flat distance
hex_socket_depth = 3.5

# --- Derived Calculations ---
# CadQuery polygon uses circumscribed diameter. 
# Formula: diameter = 2 * flat_to_flat / sqrt(3)
hex_circum_diameter = 2 * hex_socket_size / math.sqrt(3)

# --- Modeling Process ---

# 1. Create the main Shank (Base)
result = cq.Workplane("XY").circle(shank_diameter / 2.0).extrude(shank_length)

# 2. Apply chamfers to Shank
# Bottom chamfer
result = result.faces("<Z").edges().chamfer(bottom_chamfer_size)
# Top shoulder chamfer (transition to neck)
result = result.faces(">Z").edges().chamfer(shoulder_chamfer_size)

# 3. Create the Neck
# Extrude from the top flat face of the shank
result = result.faces(">Z").workplane().circle(neck_diameter / 2.0).extrude(neck_length)

# 4. Create the Head
# Extrude from the top of the neck
result = result.faces(">Z").workplane().circle(head_diameter / 2.0).extrude(head_height)

# 5. Apply details to the Head
# Fillet the top edge
result = result.faces(">Z").edges().fillet(head_top_fillet)

# Fillet the junction between Neck and Head
# We select the edge closest to the theoretical intersection point
junction_z = shank_length + neck_length
junction_selector = cq.selectors.NearestToPointSelector((neck_diameter/2.0, 0, junction_z))
result = result.edges(junction_selector).fillet(neck_head_fillet)

# 6. Cut the Hex Socket
# Create a hexagonal cut into the top face
result = result.faces(">Z").workplane() \
    .polygon(6, hex_circum_diameter) \
    .cutBlind(-hex_socket_depth)
