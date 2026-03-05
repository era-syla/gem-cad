import cadquery as cq
import math

# Parameters (M8 Socket Head Cap Screw)
pitch = 1.25
outer_r = 4.0
inner_r = 3.2
length = 30.0
head_r = 6.5
head_h = 8.0
hex_af = 6.0
hex_d = 4.0
fillet_r = 0.6

# 1. Create the Head
head = (
    cq.Workplane("XY")
    .circle(head_r)
    .extrude(head_h)
    .edges("top")
    .fillet(fillet_r)
)

# Calculate circumscribed diameter for the hexagon
hex_diam = hex_af / math.cos(math.radians(30))

# Cut the hex socket
head = (
    head.faces(">Z")
    .workplane()
    .polygon(6, hex_diam)
    .cutBlind(-hex_d)
)

# 2. Create the Shaft with simulated annular threads
pts = []
pts.append((0, 0))
pts.append((0, -length))
pts.append((inner_r, -length))

# Thread profile starting from the bottom
current_z = -length
# Start with a 45-degree chamfer up to the outer radius
current_z += (outer_r - inner_r)
pts.append((outer_r, current_z))

# Zig-zag profile for the threads
while current_z < -1e-6:
    # Slope inwards to inner_r
    next_z = current_z + pitch / 2.0
    if next_z >= 0:
        dz = 0 - current_z
        dx = (inner_r - outer_r) * (dz / (pitch / 2.0))
        pts.append((outer_r + dx, 0))
        break
    pts.append((inner_r, next_z))
    current_z = next_z
    
    # Slope outwards to outer_r
    next_z = current_z + pitch / 2.0
    if next_z >= 0:
        dz = 0 - current_z
        dx = (outer_r - inner_r) * (dz / (pitch / 2.0))
        pts.append((inner_r + dx, 0))
        break
    pts.append((outer_r, next_z))
    current_z = next_z

# Revolve the profile to create the threaded shaft
shaft = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# Combine head and shaft
result = head.union(shaft)