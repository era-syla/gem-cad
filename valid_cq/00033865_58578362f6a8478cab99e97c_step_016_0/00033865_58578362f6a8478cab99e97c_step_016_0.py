import cadquery as cq
import math

# --- Parameters for M6 Button Head Socket Cap Screw ---
# Dimensions approximated based on ISO 7380
thread_diameter = 6.0      # Nominal diameter (M6)
total_length = 30.0        # Length of the screw (shank)
head_diameter = 10.5       # Head diameter (dk)
head_height = 3.3          # Head height (k)
hex_size = 4.0             # Hex socket size across flats (s)
socket_depth = 2.5         # Depth of the hex socket
chamfer_tip = 0.5          # Chamfer size at the screw tip
fillet_under_head = 0.3    # Small fillet radius under the head

# --- Helper Math ---
# 1. Calculate the radius of curvature for the button head (Spherical Cap)
# Using the relationship: R = (h^2 + r^2) / 2h
# where h = head_height, r = head_diameter / 2
R_head = (head_height**2 + (head_diameter / 2)**2) / (2 * head_height)

# 2. Calculate the circumscribed diameter for the hexagon
# CadQuery polygon() uses the circumscribed diameter.
# d_circum = s / cos(30deg) = s / (sqrt(3)/2)
hex_circum_diameter = hex_size / (math.sqrt(3) / 2)

# --- Geometry Construction ---

# 1. Create the Button Head
# We create a sphere and position it such that the top is at z = head_height
# and the center is aligned with the Z-axis.
sphere_center_z = head_height - R_head

# Create the base sphere
head_sphere = (
    cq.Workplane("XY")
    .sphere(R_head)
    .translate((0, 0, sphere_center_z))
)

# Cut off the bottom of the sphere below Z=0 to create the flat bearing surface
# We extrude a large rectangle downwards from Z=0 to act as a cutter
cutter = (
    cq.Workplane("XY")
    .rect(head_diameter * 2, head_diameter * 2)
    .extrude(-head_diameter) # Extrude down enough to cover the sphere bottom
)

head = head_sphere.cut(cutter)

# 2. Create the Shank (Threaded portion representation)
# We model this as a cylinder. Thread texturing is omitted for CAD stability.
shank = (
    cq.Workplane("XY")
    .circle(thread_diameter / 2)
    .extrude(-total_length)
)

# 3. Combine Head and Shank
screw = head.union(shank)

# 4. Create the Hex Socket
# Cut a hexagon into the top face of the head
screw = (
    screw.faces(">Z")
    .workplane()
    .polygon(6, hex_circum_diameter)
    .cutBlind(-socket_depth)
)

# 5. Add Tip Chamfer
# Select the bottom face, then its edges
screw = (
    screw.faces("<Z")
    .edges()
    .chamfer(chamfer_tip)
)

# 6. Add Fillet under the Head
# Select the edge where the head meets the shank (at Z=0, radius approx thread_diameter/2)
# We use a selector to find the edge nearest to a point on that circle
intersection_edge_selector = cq.selectors.NearestToPointSelector((thread_diameter / 2, 0, 0))
result = screw.edges(intersection_edge_selector).fillet(fillet_under_head)

# result now contains the final solid geometry