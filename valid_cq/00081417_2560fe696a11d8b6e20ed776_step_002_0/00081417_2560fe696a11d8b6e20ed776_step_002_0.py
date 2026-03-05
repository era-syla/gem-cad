import cadquery as cq

# Dimensions
length = 100.0    # Length of the plate (X axis)
width = 80.0      # Width of the plate (Y axis)
thickness = 4.0   # Thickness of the plate
text_str = "trous" # Text content ("trous" - French for holes)
font_size = 28.0  # Size of the text
font_name = "Times New Roman" # Serif font to match the image style

# Create the base rectangular plate
# The box is centered on the origin by default
result = cq.Workplane("XY").box(length, width, thickness)

# Cut the text through the plate
# 1. Select the top face (>Z)
# 2. Create a new workplane on that face
# 3. Create the 3D text and cut it from the base
#    - distance is negative to cut into the material
#    - cut=True performs the boolean subtraction
result = result.faces(">Z").workplane().text(
    text_str,
    font_size,
    -thickness,
    font=font_name,
    cut=True,
    halign="center",
    valign="center"
)