import cadquery as cq
import math

# --- Parameters (M8 Socket Head Cap Screw) ---
M_dia = 8.0               # Nominal Shaft Diameter
head_dia = 13.0           # Head Diameter
head_height = 8.0         # Head Height
socket_size = 6.0         # Hex Socket Width (Across Flats)
socket_depth = 4.0        # Depth of the hex socket
length = 40.0             # Total Length under head
thread_len = 25.0         # Length of the threaded portion
shank_len = length - thread_len
neck_fillet = 0.6         # Radius of fillet under the head
head_chamfer = 0.5        # Chamfer size on top of head
tip_chamfer = 1.0         # Chamfer size at the tip
groove_dia = 7.2          # Minor diameter at the thread relief groove
groove_width = 1.0        # Width of the thread relief groove

# --- Modeling ---

# 1. Create the Head
# Start on XY plane, extrude upwards to create the head
result = (cq.Workplane("XY")
          .circle(head_dia / 2.0)
          .extrude(head_height))

# 2. Create the Shaft
# Select the bottom face of the head (Z=0) and extrude downwards
# The normal of the bottom face is -Z, so positive extrude length goes down.
result = (result.faces("<Z")
          .workplane()
          .circle(M_dia / 2.0)
          .extrude(length))

# 3. Cut the Hex Socket
# Calculate circumdiameter for the hexagon based on across-flats size
poly_dia = socket_size / math.cos(math.radians(30))

result = (result.faces(">Z")
          .workplane()
          .polygon(nSides=6, diameter=poly_dia)
          .cutBlind(-socket_depth))

# 4. Create Thread Relief Groove
# Create a temporary solid ring to subtract from the shaft at the shank/thread junction.
# Positioned at Z = -shank_len
groove_tool = (cq.Workplane("XY")
               .workplane(offset=-shank_len)
               .circle(M_dia)            # Outer boundary (larger than shaft)
               .circle(groove_dia / 2.0) # Inner boundary (groove bottom)
               .extrude(-groove_width, combine=False)) # Extrude down, create separate solid

result = result.cut(groove_tool)

# 5. Apply Details (Fillets and Chamfers)

# Neck Fillet (Junction of head and shaft at Z=0)
# Select edge near the shaft surface at Z=0
result = result.edges(cq.selectors.NearestToPointSelector((M_dia/2.0, 0, 0))).fillet(neck_fillet)

# Head Top Chamfer (Outer edge of the head at Z=head_height)
result = result.edges(cq.selectors.NearestToPointSelector((head_dia/2.0, 0, head_height))).chamfer(head_chamfer)

# Shaft Tip Chamfer (Bottom edge of the shaft at Z=-length)
result = result.edges(cq.selectors.NearestToPointSelector((M_dia/2.0, 0, -length))).chamfer(tip_chamfer)