import cadquery as cq

# Parametric dimensions based on visual analysis and standard hardware logic
shaft_diameter = 8.0
shaft_length = 20.0
head_diameter = 11.5
head_height = 5.5
text_content = "8-20"
text_fontsize = 4.5
text_thickness = 1.0

# Create the shaft (base cylinder)
result = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(shaft_length)

# Create the head (larger cylinder on top)
result = result.faces(">Z").workplane().circle(head_diameter / 2.0).extrude(head_height)

# Create the embossed text on the top face
# cut=False creates a solid (emboss), combine=True merges it with the head
result = result.faces(">Z").workplane().text(
    text_content, 
    fontsize=text_fontsize, 
    distance=text_thickness, 
    cut=False, 
    combine=True
)