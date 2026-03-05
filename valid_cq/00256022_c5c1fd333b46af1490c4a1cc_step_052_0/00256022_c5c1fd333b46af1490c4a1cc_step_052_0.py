import cadquery as cq
import math

# --- Parameters (Standard M6 Socket Head Cap Screw dimensions) ---
thread_dia = 6.0          # Nominal thread diameter
length = 40.0             # Shank length
head_dia = 10.0           # Head diameter
head_height = 6.0         # Head height
socket_size = 5.0         # Hex socket width across flats
socket_depth = 3.5        # Depth of the hex socket
fillet_radius = 0.4       # Radius for the fillet under the head
chamfer_size = 0.5        # Chamfer size for head top and shank tip

# Calculate circumdiameter for the hexagon (required for cq.polygon)
# Formula: Diameter = Width_Across_Flats / (sqrt(3) / 2)
hex_outer_dia = socket_size / (math.sqrt(3) / 2.0)

# --- Modeling ---

# 1. Create the Head
# Establish Z=0 as the contact surface between head and shank
result = (
    cq.Workplane("XY")
    .circle(head_dia / 2.0)
    .extrude(head_height)
)

# 2. Create the Shank
# Select the bottom face of the head (Z=0) and extrude downwards
result = (
    result.faces("<Z")
    .workplane()
    .circle(thread_dia / 2.0)
    .extrude(length)
)

# 3. Cut the Hex Socket
# Select the top face of the head and cut the hexagonal recess
result = (
    result.faces(">Z")
    .workplane()
    .polygon(6, hex_outer_dia)
    .cutBlind(-socket_depth)
)

# 4. Finishing Details

# Chamfer the top outer edge of the head
# Select edge closest to the outer rim on the top plane
result = result.edges(
    cq.selectors.NearestToPointSelector((head_dia / 2.0, 0, head_height))
).chamfer(chamfer_size)

# Chamfer the bottom tip of the shank
# Select edge closest to the outer rim on the bottom plane
# Note: Since we extruded 'length' from the bottom face (normal -Z), 
# the coordinate is roughly -length relative to the Z=0 plane.
result = result.edges(
    cq.selectors.NearestToPointSelector((thread_dia / 2.0, 0, -length))
).chamfer(chamfer_size)

# Fillet the neck (transition between head and shank)
# Select the edge at Z=0 with the diameter of the shank
result = result.edges(
    cq.selectors.NearestToPointSelector((thread_dia / 2.0, 0, 0))
).fillet(fillet_radius)