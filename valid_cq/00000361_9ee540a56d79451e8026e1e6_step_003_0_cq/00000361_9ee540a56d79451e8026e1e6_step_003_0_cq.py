import cadquery as cq

# --- Parametric Dimensions ---
plate_width = 100.0   # Width of the base plate
plate_height = 80.0   # Height (depth) of the base plate
plate_thickness = 1.0 # Thickness of the base plate

text_string = "Onshape"
text_size = 12.0      # Font size
text_height = 2.0     # Height of the embossed text
font_name = "Arial"   # Standard sans-serif font usually available

# Positioning relative to center
# Based on the image, the text is in the lower-right quadrant, rotated
# Let's adjust coordinate system to place it reasonably
text_pos_x = plate_width / 4.0
text_pos_y = -plate_height / 3.0

# --- Geometry Construction ---

# 1. Create the base plate
# Centered on XY plane for easier symmetric positioning later if needed
base_plate = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Create the text
# We need to position the workplane on top of the plate
# The text needs to be rotated 180 degrees based on the visual perspective 
# (reading "Onshape" upside down relative to the standard isometric view implies rotation)
# or simply placed and oriented. Looking at the image, if the near corner is bottom-left,
# the text is on the right edge, rotated 90 degrees or -90 degrees.
# Let's try to match the visual orientation:
# The text "Onshape" runs along the short edge.

text_layer = (
    base_plate.faces(">Z").workplane()
    .center(35, 0) # Shift towards the right edge
    .transformed(rotate=(0, 0, 90)) # Rotate to run along the edge
    .text(text_string, text_size, text_height, font=font_name, combine=True)
)

# Combine the plate and the text
result = text_layer

# Export/Visualization (optional, but good for checking)
# cq.exporters.export(result, "result.step")