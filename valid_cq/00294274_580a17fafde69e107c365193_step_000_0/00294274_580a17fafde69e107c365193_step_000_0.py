import cadquery as cq

# Parameters for the text model
text_content = "THE"
font_size = 10.0
thickness = 1.0
font_name = "Arial"  # Using a simple sans-serif font to match the image

# Create the 3D text geometry
# We create a workplane on the XY plane and generate extruded text
result = (
    cq.Workplane("XY")
    .text(
        text_content,
        font_size,
        thickness,
        font=font_name,
        halign="center",
        valign="center"
    )
)