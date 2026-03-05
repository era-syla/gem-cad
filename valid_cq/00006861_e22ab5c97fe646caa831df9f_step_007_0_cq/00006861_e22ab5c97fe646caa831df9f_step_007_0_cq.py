import cadquery as cq

# Define parameters for the model
plate_length = 50.0  # Length of the base plate
plate_width = 30.0   # Width of the base plate
plate_thickness = 3.0 # Thickness of the base plate
text_string = "DSS"
text_size = 12.0     # Font size of the text
text_height = 1.0    # Height of the embossed text
font_name = "Arial"  # Standard sans-serif font

# Create the base plate
# We center it on the XY plane for easier positioning
base_plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Create the text
# We create a new workplane on the top face of the base plate
# We center the text on the plate
text_emboss = (
    base_plate.faces(">Z")
    .workplane()
    .text(text_string, fontsize=text_size, distance=text_height, font=font_name, halign="center", valign="center")
)

# Combine the base plate and the text (text() operation usually combines automatically, 
# but ensuring 'result' holds the complete solid)
result = text_emboss

# Export or display is handled by the environment, but 'result' is the requested variable.