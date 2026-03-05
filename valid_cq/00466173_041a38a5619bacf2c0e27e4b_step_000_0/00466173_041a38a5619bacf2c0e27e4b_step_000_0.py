import cadquery as cq

# Parametric dimensions
head_width = 20.0         # Width of the square cross-section (before chamfering)
head_length = 15.0        # Axial length of the head
shaft_diameter = 6.0      # Diameter of the cylindrical shaft
shaft_length = 90.0       # Length of the cylindrical shaft

# Calculate chamfer distance to create a regular octagon from a square
# Formula for regular octagon side 's' from width 'w': s = w / (1 + sqrt(2))
# Chamfer 'c' is: c = (w - s) / 2 = w / (2 + sqrt(2))
chamfer_size = head_width / (2 + 2**0.5)

# Generate the 3D model
result = (
    cq.Workplane("YZ")
    # 1. Create the head as a square prism first
    .rect(head_width, head_width)
    .extrude(head_length)
    
    # 2. Chamfer the longitudinal edges to form the octagonal profile
    # Select edges parallel to the X axis (extrusion direction)
    .edges("|X")
    .chamfer(chamfer_size)
    
    # 3. Create the shaft attached to the back of the head
    # Select the face at the minimum X coordinate (the starting face of the extrusion)
    .faces("<X")
    .workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)