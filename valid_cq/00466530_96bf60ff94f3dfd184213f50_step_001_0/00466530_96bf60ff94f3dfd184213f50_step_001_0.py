import cadquery as cq

# Parametric dimensions
text_content = "Keepin"
font_size = 25.0       # Height of the text
extrusion_depth = 8.0  # Thickness of the text
font_name = "Arial"    # Sans-serif font to match the style

# Generate the 3D text model
# Note: The specific separation of the 'K' parts depends on the specific font file used.
# Standard Arial is used here as a close approximation.
result = (
    cq.Workplane("XY")
    .text(
        text_content,
        font_size,
        extrusion_depth,
        font=font_name,
        halign="center",
        valign="center"
    )
)