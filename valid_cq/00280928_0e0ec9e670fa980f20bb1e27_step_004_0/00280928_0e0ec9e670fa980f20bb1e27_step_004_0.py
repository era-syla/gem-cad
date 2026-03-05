import cadquery as cq

# Parametric dimensions
width = 4.0          # Cross-section width/height
l_start_y = 12.0     # Initial leg along Y
l_conn_x = 15.0      # Connector along X
l_long_y = 100.0     # Long main section along Y
l_drop_z = 30.0      # Vertical drop
l_mid_x = 35.0       # Middle section along X
l_end_y = 35.0       # End section along Y
l_tip_z = 10.0       # Final tip drop

# Define the 3D path points
# Starting at origin (0,0,0)
points = []
x, y, z = 0.0, 0.0, 0.0
points.append((x, y, z))

# 1. Start segment along +Y
y += l_start_y
points.append((x, y, z))

# 2. Connector along +X
x += l_conn_x
points.append((x, y, z))

# 3. Long section along +Y
y += l_long_y
points.append((x, y, z))

# 4. Vertical drop along -Z
z -= l_drop_z
points.append((x, y, z))

# 5. Middle section along +X
x += l_mid_x
points.append((x, y, z))

# 6. End section along +Y
y += l_end_y
points.append((x, y, z))

# 7. Final tip along -Z
z -= l_tip_z
points.append((x, y, z))

# Build the path wire from edges
edges = []
for i in range(len(points) - 1):
    p1 = cq.Vector(points[i])
    p2 = cq.Vector(points[i+1])
    edges.append(cq.Edge.makeLine(p1, p2))

path_wire = cq.Wire.assembleEdges(edges)
path = cq.Workplane().newObject([path_wire])

# Create the square profile and sweep
# Path starts along Y axis, so profile must be on XZ plane
result = (
    cq.Workplane("XZ")
    .rect(width, width)
    .sweep(path)
)