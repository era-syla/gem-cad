import cadquery as cq

# Parametric dimensions for the model
shaft_diameter = 12.0
shaft_length = 35.0
head_diameter = 20.0
head_height = 12.0
text_string = "0Z-8"
text_size = 9.0
text_thickness = 2.0

# Generate the 3D model
# 1. Create the shaft cylinder starting from the XY plane
result = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(shaft_length)

# 2. Create the head cylinder on top of the shaft
result = (
    result.faces(">Z")
    .workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_height)
)

# 3. Create the embossed text on the top face of the head
# cut=False ensures the text is added (extruded) rather than removed
result = (
    result.faces(">Z")
    .workplane()
    .text(text_string, fontsize=text_size, distance=text_thickness, cut=False)
)