import cadquery as cq

# Parameters for the text model
text_string = "Materialix"
font_size = 10.0
thickness = 1.5
font_family = "Times New Roman"  # Serif font to match the image style

# Create the 3D text geometry
# The text function creates a solid extrusion of the specified string
result = cq.Workplane("XY").text(
    text_string,
    font_size,
    thickness,
    font=font_family,
    halign="center",
    valign="center"
)