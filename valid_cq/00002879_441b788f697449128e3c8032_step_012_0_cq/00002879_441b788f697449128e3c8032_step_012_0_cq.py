import cadquery as cq

# Parametric dimensions (based on a standard M6 Socket Head Cap Screw)
head_diameter = 10.0
head_height = 6.0
shaft_diameter = 6.0
shaft_length = 15.0
hex_socket_size = 5.0  # Across flats (usually shaft_diameter - 1mm or similar)
hex_socket_depth = 3.5
fillet_radius = 0.5    # Radius for the top edge of the head
chamfer_size = 0.5     # Chamfer at the bottom of the shaft

# 1. Create the Head
# Start with a cylinder for the head
head = cq.Workplane("XY").circle(head_diameter / 2).extrude(head_height)

# 2. Create the Shaft
# Extrude the shaft from the bottom of the head
# We select the bottom face (<Z) and draw the shaft circle
shaft = (
    head.faces("<Z")
    .workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# 3. Create the Hex Socket
# Select the top face (>Z) and cut a hexagon
# We use polygon(6, ...) for a hexagon. The size parameter in CadQuery's polygon 
# is usually the diameter of the circumscribed circle. 
# For a hex 'across flats' (s), the circumscribed diameter (d) is d = s / cos(30) = s / (sqrt(3)/2) ~ s * 1.1547
circumscribed_diameter = hex_socket_size / 0.866025
result_with_socket = (
    shaft.faces(">Z")
    .workplane()
    .polygon(6, circumscribed_diameter)
    .cutBlind(-hex_socket_depth)
)

# 4. Finishing Touches (Fillets and Chamfers)
# Fillet the top edge of the head
# We select the edges on the top face (but not the inner hex edges).
# The easiest way is to select edges of the top face that are circular.
result = (
    result_with_socket
    .edges(f" %Circle and >Z") # Select circular edges at the very top
    .fillet(fillet_radius)
)

# Chamfer the bottom of the shaft for easier insertion
result = (
    result.edges("<Z") # Select the bottom-most edge
    .chamfer(chamfer_size)
)

# Optional: Add a small fillet under the head for stress relief (standard on screws)
# This selects the edge where the head meets the shaft
result = result.edges(cq.selectors.RadiusNthSelector(1)).fillet(0.2)
# Note: RadiusNthSelector(0) is the shaft chamfer (smallest radius), 
# RadiusNthSelector(1) is the shaft radius. We need to be careful with selection.
# A robust way is to select edges at the Z height of the head bottom.
# Z = head_height (if we started at Z=0 and went up, but we extruded down for shaft).
# Let's verify coordinates:
# Head is Z=0 to Z=6. Shaft starts at Z=0 and extrudes to Z=15 (local direction) -> Global Z=0 to Z=-15.
# Wait, the second extrude (shaft) creates a new solid fused to the first.
# Coordinates: Head top is Z=6, Head bottom is Z=0. Shaft bottom is Z=-15.
# So the neck is at Z=0.
result = result.edges(cq.selectors.NearestToPointSelector((0, 0, 0))).fillet(0.2)

# Export or visualization
if 'show_object' in globals():
    show_object(result)