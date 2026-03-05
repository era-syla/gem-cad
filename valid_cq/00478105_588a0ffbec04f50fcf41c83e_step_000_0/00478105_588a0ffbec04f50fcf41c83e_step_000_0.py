import cadquery as cq
import math

# --- Parametric Dimensions (based on M6 Socket Head Cap Screw) ---
M_SIZE = 6.0                # Shaft diameter
HEAD_DIA = 10.0             # Head diameter
HEAD_HEIGHT = 6.0           # Head height
SHANK_LENGTH = 20.0         # Length of the shaft
SOCKET_FLATS = 5.0          # Hex key size (across flats)
SOCKET_DEPTH = 3.5          # Depth of the hexagonal socket
CHAMFER_SIZE = 0.5          # Chamfer at the screw tip

# Calculate the circumscribed diameter for the hexagon
# For a hexagon, circum_diameter = flats / cos(30 degrees)
hex_circum_dia = SOCKET_FLATS / math.cos(math.radians(30))

# --- Geometric Construction ---

# 1. Create the cylindrical head
result = cq.Workplane("XY").circle(HEAD_DIA / 2.0).extrude(HEAD_HEIGHT)

# 2. Cut the hexagonal socket into the top face
result = (
    result.faces(">Z")              # Select the top face of the head
    .workplane()
    .polygon(6, hex_circum_dia)     # Create hexagon profile
    .cutBlind(-SOCKET_DEPTH)        # Cut into the head
)

# 3. Extrude the shank from the bottom of the head
# Note: Extruding from a face extends along the face normal.
# The bottom face normal points downwards (-Z).
result = (
    result.faces("<Z")              # Select the bottom face of the head
    .workplane()
    .circle(M_SIZE / 2.0)           # Create shaft profile
    .extrude(SHANK_LENGTH)          # Extrude shaft
)

# 4. Chamfer the tip of the screw
result = (
    result.faces("<Z")              # Select the new bottom face (tip of shaft)
    .edges()                        # Select edges of this face
    .chamfer(CHAMFER_SIZE)          # Apply chamfer
)