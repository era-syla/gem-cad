import cadquery as cq

# Parameters for the model
text_content = "Jenna"
font_size = 12.0
text_extrusion = 2.0
base_thickness = 3.0
margin_x = 3.0
margin_y = 3.0
font_name = "Times New Roman"  # Serif font to match the visual style of the image

# 1. Create the 3D Text
# The text is created on the XY plane and extruded upwards
text_geo = cq.Workplane("XY").text(
    text_content,
    font_size,
    text_extrusion,
    font=font_name,
    kind="bold",
    halign="center",
    valign="center"
)

# 2. Determine the bounding box of the text to automatically size the base plate
bb = text_geo.val().BoundingBox()
base_length = bb.xlen + (margin_x * 2)
base_width = bb.ylen + (margin_y * 2)

# 3. Create the base plate
# Using .box() creates a centered box at (0,0,0)
# We translate it down so its top face lies on the Z=0 plane (aligning with text bottom)
base = cq.Workplane("XY").box(base_length, base_width, base_thickness)\
    .translate((0, 0, -base_thickness / 2))

# 4. Union the text and the base into a single solid
part = base.union(text_geo)

# 5. Mirror the part to create the stamp effect (reversed text)
# Mirroring across YZ plane flips the X-axis, making "Jenna" read backwards as in the image
result = part.mirror("YZ")