import cadquery as cq

# --- Parametric Dimensions ---
# Standard M6 socket head cap screw dimensions (approximate)
# These can be adjusted to generate different sizes
head_diameter = 10.0  # Diameter of the screw head
head_height = 6.0     # Height of the screw head
shaft_diameter = 6.0  # Diameter of the threaded part (M6)
shaft_length = 12.0   # Length of the shaft
hex_socket_size = 5.0 # Distance across flats for the hex key (standard for M6 is 5mm)
hex_socket_depth = 3.5 # Depth of the hex socket

# --- Modeling ---

# 1. Create the head
# We start with a simple cylinder for the head
head = cq.Workplane("XY").circle(head_diameter / 2).extrude(head_height)

# 2. Create the shaft
# We extrude the shaft from the bottom of the head
# Note: We extrude in the negative direction relative to the head's base
shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2)
    .extrude(-shaft_length)
)

# 3. Create the hex socket
# We create a hexagon on the top face of the head and cut it downwards
# polygon(6, ...) creates a hexagon. The size is typically the diameter of the circumcircle.
# For a hex key size 's' (across flats), the circumradius 'R' is s / sqrt(3).
# However, cq.Workplane.polygon usually takes the circumdiameter or radius depending on implementation,
# often defined by the diameter of the circle encompassing the points.
# Let's use the 'diameter' parameter of polygon which usually refers to the circumdiameter.
# circumdiameter = (hex_socket_size / cos(30 degrees)) = hex_socket_size / (sqrt(3)/2) * 2 / 2 ... wait.
# circumradius = hex_socket_size / (2 * cos(30)) = hex_socket_size / sqrt(3)
# circumdiameter = 2 * hex_socket_size / sqrt(3)

import math
circum_diameter = 2 * (hex_socket_size / (2 * math.cos(math.radians(30))))

socket_cut = (
    head.faces(">Z")
    .workplane()
    .polygon(6, circum_diameter)
    .cutBlind(-hex_socket_depth)
)

# 4. Combine head and shaft
# Since we created the shaft separately relative to the origin, and the head relative to the origin,
# they are already positioned correctly relative to the Z=0 plane (Head goes 0 to +6, Shaft goes 0 to -12).
# We unite them into a single solid.

result = socket_cut.union(shaft)

# --- Final Export/Display ---
# In a typical CadQuery environment, 'result' is the variable to be rendered.