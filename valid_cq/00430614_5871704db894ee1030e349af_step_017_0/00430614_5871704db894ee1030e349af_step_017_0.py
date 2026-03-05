import cadquery as cq
import math

# Dimensions for a standard M6 Socket Head Cap Screw
head_diameter = 10.0      # dk
head_height = 6.0         # k
shank_diameter = 6.0      # d
shank_length = 25.0       # l
hex_size = 5.0            # s (width across flats)
socket_depth = 3.0        # t
head_chamfer = 0.5
tip_chamfer = 0.5

# Calculate the diameter of the circumscribed circle for the hex polygon
# Relation: Across Flats (s) = Diameter * (sqrt(3)/2)
hex_outer_diameter = hex_size * 2.0 / math.sqrt(3)

# 1. Create the cylindrical head
# We start on the XY plane and extrude upwards
result = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(head_height)

# 2. Chamfer the top edge of the head
# Select the top face (>Z), get its edges (the outer circle), and chamfer
result = result.faces(">Z").edges().chamfer(head_chamfer)

# 3. Cut the hexagonal socket
# Create a workplane on the top face, draw a polygon, and cut downwards
result = (
    result.faces(">Z")
    .workplane()
    .polygon(6, hex_outer_diameter)
    .cutBlind(-socket_depth)
)

# 4. Create the shank
# Select the bottom face of the head (<Z), draw the shank circle, and extrude
# The workplane on the bottom face has its normal pointing -Z, 
# so a positive extrusion length extends downwards.
result = (
    result.faces("<Z")
    .workplane()
    .circle(shank_diameter / 2.0)
    .extrude(shank_length)
)

# 5. Chamfer the tip of the screw
# Select the new bottom-most face and chamfer its edges
result = result.faces("<Z").edges().chamfer(tip_chamfer)