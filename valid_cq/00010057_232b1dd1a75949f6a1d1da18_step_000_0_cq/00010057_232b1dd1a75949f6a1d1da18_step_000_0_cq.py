import cadquery as cq

# Parameters for the text
text_string_1 = "GreatTextTool!"  # The top line of text (read backwards in image)
text_string_2 = "ClearVision Lighting" # The bottom line of text (read backwards in image)

font_name = "Arial"      # A standard sans-serif font
font_size_1 = 10.0       # Size for the top text
font_size_2 = 5.0        # Size for the bottom text (smaller)
text_thickness = 2.0     # Extrusion depth
spacing_y = 12.0         # Distance between the two lines of text

# Create the top line of text
# We use extrude to give it 3D depth. 
# The image shows mirrored text, which often happens when looking at the "back" of a sign 
# or if the text is intended for a mold. To replicate the image exactly as seen, 
# we will mirror it across the YZ plane (flipping X) after creation.
text1 = (
    cq.Workplane("XY")
    .text(text_string_1, font_size_1, text_thickness, font=font_name, halign="center", valign="bottom")
)

# Create the bottom line of text
# We offset the workplane in Y to position it below the first line
text2 = (
    cq.Workplane("XY")
    .center(0, -spacing_y) # Move down
    .text(text_string_2, font_size_2, text_thickness, font=font_name, halign="center", valign="top")
)

# Combine the two text objects
combined_text = text1.union(text2)

# To match the visual perspective of the provided image where the text appears backwards
# (like looking in a mirror or at a stamp), we mirror the result across the YZ plane.
result = combined_text.mirror(mirrorPlane="YZ")

# Alternatively, if you just want the text readable:
# result = combined_text 