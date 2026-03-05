import cadquery as cq

# Parameters for the Socket Head Cap Screw (approximate M6 dimensions used as defaults)
head_diameter = 10.0
head_height = 6.0
shank_diameter = 6.0
shank_length = 12.0
hex_socket_size = 5.0  # Distance across flats
hex_socket_depth = 3.5
head_fillet = 0.5     # Fillet radius on top edge of head
tip_chamfer = 0.5     # Chamfer at the end of the screw

# 1. Create the head
# We start with the basic cylindrical shape of the head
head = cq.Workplane("XY").circle(head_diameter / 2).extrude(head_height)

# 2. Add the shank
# We create the shank cylinder below the head
shank = (
    cq.Workplane("XY")
    .workplane(offset=0)  # Start at the base of the head
    .circle(shank_diameter / 2)
    .extrude(-shank_length) # Extrude downwards
)

# Combine head and shank
bolt_body = head.union(shank)

# 3. Create the hex socket cut
# Draw a polygon (6 sides for hex) on the top face
bolt_with_socket = (
    bolt_body.faces(">Z")
    .workplane()
    .polygon(nSides=6, diameter=hex_socket_size / 0.866025) # converting flat-to-flat to diameter (circumscribed)
    .cutBlind(-hex_socket_depth)
)

# 4. Add finishing touches (fillets and chamfers)
# Fillet the top outer edge of the head
result = bolt_with_socket.edges(">Z").fillet(head_fillet)

# Chamfer the bottom edge of the shank (screw tip)
result = result.edges("<Z").chamfer(tip_chamfer)

# (Optional) Small chamfer or fillet where shank meets head for stress relief
# This is common in real bolts but might not be strictly visible in the simplified render.
# result = result.edges(cq.selectors.RadiusNthSelector(1)).fillet(0.2) 

# Export or display the result
# show_object(result)