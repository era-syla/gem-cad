import cadquery as cq

# Parametric dimensions for the button head hex screw
d_shaft = 6.0          # Shaft diameter
l_shaft = 18.0         # Shaft length
d_head = 10.5          # Head diameter
h_head = 3.3           # Head total height
head_fillet = 2.0      # Radius of the head dome fillet
d_hex = 4.6            # Circumscribed diameter of the hex socket
depth_hex = 2.0        # Depth of the hex socket

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # Create the cylindrical shaft (extruded downwards)
    .circle(d_shaft / 2.0)
    .extrude(-l_shaft)
    # Move to the top face of the shaft to create the head
    .faces(">Z")
    .workplane()
    .circle(d_head / 2.0)
    .extrude(h_head)
    # Fillet the top edge to create the button head profile
    .edges(">Z")
    .fillet(head_fillet)
    # Create the hex socket cut on the top face
    .faces(">Z")
    .workplane()
    .polygon(6, d_hex)
    .cutBlind(-depth_hex)
)