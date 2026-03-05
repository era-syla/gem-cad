import cadquery as cq

# Geometric parameters based on visual estimation
plate_length = 90.0
plate_width = 35.0
plate_thickness = 2.0

text_string = "grainne"
font_size = 18.0
text_extrusion = 2.0

# 1. Create the base rectangular plate centered on the XY plane
# The box method creates a box with the specified dimensions
base_plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Create the embossed text on the top surface
# - Select the top face using faces(">Z")
# - Create a new workplane on that face
# - Use the text() method to generate the letters
# - cut=False ensures the text is added (embossed) rather than subtracted
# - combine=True unites the text with the base plate
result = base_plate.faces(">Z").workplane().text(
    text_string,
    fontsize=font_size,
    distance=text_extrusion,
    cut=False,
    combine=True,
    halign="center",
    valign="center",
    font="Arial"
)