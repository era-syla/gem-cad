import cadquery as cq

# Parameters for the text model
text_string = "NOW"
font_size = 20.0       # The height of the text characters
extrusion_depth = 12.0 # The thickness of the 3D letters
font_name = "Arial"    # Standard sans-serif font to match the image style

# Generate the 3D text geometry
# We create a workplane on XY and extrude the text along the Z axis
result = (
    cq.Workplane("XY")
    .text(
        text_string,
        fontsize=font_size,
        distance=extrusion_depth,
        font=font_name,
        halign="center",
        valign="center"
    )
)