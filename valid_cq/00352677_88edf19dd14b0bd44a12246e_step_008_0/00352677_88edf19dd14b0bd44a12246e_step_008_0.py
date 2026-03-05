import cadquery as cq
import math

# Parameters for the Socket Head Cap Screw
# Modeled approximately as an M8 x 45 screw based on visual proportions
thread_diameter = 8.0
head_diameter = 13.0
head_height = 8.0
shank_length = 15.0      # Length of the smooth unthreaded section
thread_length = 30.0     # Length of the threaded section
hex_width = 6.0          # Width across flats for the socket
hex_depth = 4.0          # Depth of the socket
chamfer_head = 0.5       # Chamfer size for the head top
chamfer_tip = 0.8        # Chamfer size for the screw tip

# Calculate the circumscribed diameter of the hexagon (across corners)
# Relationship: width = sqrt(3) * radius
# diameter = 2 * radius = 2 * width / sqrt(3)
hex_circum_diameter = 2 * hex_width / math.sqrt(3)

# 1. Create the cylindrical head
# Start on the XY plane and extrude upwards
result = (
    cq.Workplane("XY")
    .circle(head_diameter / 2.0)
    .extrude(head_height)
)

# 2. Create the unthreaded shank
# Select the bottom face of the head and extrude downwards
# The separation into shank and thread creates the cosmetic line seen in the image
result = (
    result.faces("<Z")
    .workplane()
    .circle(thread_diameter / 2.0)
    .extrude(shank_length)
)

# 3. Create the threaded section (represented as a cylinder)
# Select the bottom of the shank and extrude further
result = (
    result.faces("<Z")
    .workplane()
    .circle(thread_diameter / 2.0)
    .extrude(thread_length)
)

# 4. Cut the hexagonal socket
# Select the top face of the head
# cutBlind with negative value cuts into the material relative to the face normal
result = (
    result.faces(">Z")
    .workplane()
    .polygon(6, hex_circum_diameter)
    .cutBlind(-hex_depth)
)

# 5. Add Chamfers
# Chamfer the top outer edge of the head
# We filter edges on the top face to select only the Circle (outer edge), ignoring the hexagon lines
result = (
    result.faces(">Z")
    .edges("%CIRCLE")
    .chamfer(chamfer_head)
)

# Chamfer the bottom tip of the screw
result = (
    result.faces("<Z")
    .edges()
    .chamfer(chamfer_tip)
)