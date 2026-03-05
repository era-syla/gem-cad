import cadquery as cq

# Geometric parameters
shaft_length = 200.0  # Total length of the shaft
shaft_diameter = 6.0  # Diameter of the shaft
chamfer_size = 0.5    # Size of the chamfer on both ends

# Create the shaft geometry
result = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
    # Select the faces at the minimum and maximum Z coordinates (ends of the cylinder)
    .faces("<Z or >Z")
    # Get the edges of those faces
    .edges()
    # Apply a chamfer for easier insertion/handling
    .chamfer(chamfer_size)
)