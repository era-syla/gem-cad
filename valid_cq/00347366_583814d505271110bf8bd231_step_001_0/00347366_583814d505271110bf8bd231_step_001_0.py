import cadquery as cq

# Parameters definition
text_string = "We are a Team"
font_size = 12.0
extrusion_thickness = 2.0

# Create the 3D text model
# We define a workplane on the XY plane and use the text method to generate solid geometry.
# The text is automatically centered and extruded to the specified thickness.
result = cq.Workplane("XY").text(
    text_string, 
    font_size, 
    extrusion_thickness
)