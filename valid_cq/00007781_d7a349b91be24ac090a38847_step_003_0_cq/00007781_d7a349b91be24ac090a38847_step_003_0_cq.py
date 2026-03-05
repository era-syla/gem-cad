import cadquery as cq

# --- Parametric Dimensions ---
# Overall plate dimensions
plate_width = 180.0
plate_height = 40.0
plate_thickness = 3.0

# Border and recess dimensions
border_width = 3.0
recess_depth = 1.5
fillet_radius = 2.0  # Outer corner fillet

# Text parameters
text_string = "Justin Evans"
text_size = 20.0     # Height of the font
text_thickness = 2.0 # How much the text sticks up from the recess floor
font_name = "Serif"  # A generic serif font to match the style

# --- Modeling Process ---

# 1. Create the base plate
base_plate = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 2. Create the recessed area
# We select the top face, sketch a rectangle offset by the border width, and cut down
recess = (
    base_plate.faces(">Z")
    .workplane()
    .rect(plate_width - 2 * border_width, plate_height - 2 * border_width)
    .cutBlind(-recess_depth)
)

# 3. Create the 3D Text
# The text needs to be placed on the floor of the recess.
# Since the box is centered on Z=0, the top face is at Z=plate_thickness/2.
# The floor of the recess is at Z = (plate_thickness/2) - recess_depth.
recess_floor_z = (plate_thickness / 2) - recess_depth

# We draw the text on a plane located at the recess floor height.
# Note: Text centering in CadQuery can sometimes be tricky depending on the font.
# We combine the text with the existing geometry.
text_obj = (
    cq.Workplane("XY")
    .workplane(offset=recess_floor_z)
    .text(text_string, fontsize=text_size, distance=text_thickness, font=font_name, halign="center", valign="center")
)

# 4. Combine geometry
# Union the base plate (with recess) and the text
result = recess.union(text_obj)

# Export (Optional, for debugging or viewing)
# cq.exporters.export(result, "nameplate.stl")