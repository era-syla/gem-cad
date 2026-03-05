import cadquery as cq

# Socket head cap screw
# Parameters
head_diameter = 10.0
head_height = 10.0
shank_diameter = 6.0
shank_length = 30.0
hex_size = 5.0  # across flats for hex socket
hex_depth = 6.0

# Build the screw body
# Start with the shank
shank = (
    cq.Workplane("XY")
    .circle(shank_diameter / 2)
    .extrude(shank_length)
)

# Build the head on top of the shank
head = (
    cq.Workplane("XY")
    .workplane(offset=shank_length)
    .circle(head_diameter / 2)
    .extrude(head_height)
)

# Combine shank and head
result = shank.union(head)

# Add fillet at bottom of head where it meets the shank
# Select edges at the junction between head and shank
try:
    result = result.edges(
        cq.selectors.NearestToPointSelector((0, 0, shank_length))
    ).fillet(0.5)
except:
    pass

# Add chamfer at top of head
try:
    result = result.faces(">Z").edges().chamfer(0.5)
except:
    pass

# Add chamfer at bottom of shank
try:
    result = result.faces("<Z").edges().chamfer(0.3)
except:
    pass

# Cut the hex socket into the top of the head
hex_socket = (
    cq.Workplane("XY")
    .workplane(offset=shank_length + head_height)
    .polygon(6, hex_size)
    .extrude(hex_depth)
)

result = result.cut(hex_socket)

# Add a small fillet to the top edge of the hex socket opening
# (skip fillet on internal hex as it causes issues)

result = result