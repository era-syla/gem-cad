import cadquery as cq

# Parameters for the text
text_string = "BASS"
font_name = "Arial"  # Standard font, should be available on most systems
font_size = 20       # Size of the letters
font_thickness = 10  # Depth of the extrusion
letter_spacing = 20  # Vertical spacing between letters

# Create the workplane
wp = cq.Workplane("XY")

# List to hold the individual letter solids
letters = []

# Loop through each character in the string
for i, char in enumerate(text_string):
    # Calculate the Y position for the current letter.
    # We stack them vertically, so we subtract spacing for each subsequent letter.
    # Adjusting position so the first letter is at the top.
    y_pos = -i * letter_spacing
    
    # Create the 3D text for the single character
    # We use halign="center" and valign="center" to make positioning easier
    letter = (
        cq.Workplane("XY")
        .center(0, y_pos)
        .text(
            char, 
            fontsize=font_size, 
            distance=font_thickness, 
            font=font_name,
            halign="center", 
            valign="center"
        )
    )
    letters.append(letter)

# Combine all letters into a single object
# Start with the first letter and union the rest
result = letters[0]
for letter in letters[1:]:
    result = result.union(letter)

# Optional: Rotate for better viewing orientation similar to the image
# The image shows the text standing up, possibly rotated.
# Let's align it so it lays flat on XY or stands up depending on preference.
# The default text extrusion is along Z.
# Let's leave it in the default orientation where Z is the thickness.