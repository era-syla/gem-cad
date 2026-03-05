import cadquery as cq

# Parameters
plate_length = 200.0
plate_width = 50.0
plate_thickness = 5.0
recess_depth = 2.0
rim_width = 3.0
text_string = "James McElroy"
text_size = 20.0  # Height of the text
text_thickness = 3.0 # How much the text sticks up from the recessed floor

# 1. Create the base plate
# We start with a solid rectangular box.
base = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Create the recess (pocket)
# We select the top face, offset inward by the rim width, and cut down.
# The offset is negative to go inward.
recessed_plate = (
    base.faces(">Z")
    .workplane()
    .rect(plate_length - 2 * rim_width, plate_width - 2 * rim_width)
    .cutBlind(-recess_depth)
)

# 3. Create the text
# We need to position the text on the floor of the recess.
# The floor is at Z = plate_thickness/2 - recess_depth.
# However, using the "faces" selector is more robust.
# We select the large flat face inside the recess.
# The text needs to be centered.

# Find the recessed face (it's the second highest Z face usually, or we can select by Z coordinate)
# Strategy: Select the top face of the original box, go down by recess_depth, establish workplane.
text_plane = recessed_plate.faces(">Z[-2]").workplane()

# Note: Depending on the specific font available on the system, the look might vary.
# "Arial" is a safe default, but "Serif" or "Times New Roman" matches the image better.
# CadQuery uses system fonts. We will stick to the default or a generic serif if possible,
# but usually, just specifying the string is enough.
# The image shows a serif font.

result = (
    text_plane
    .text(
        text_string,
        fontsize=text_size,
        distance=text_thickness,
        font="Serif",  # Attempt to match the style in the image
        kind="regular",
        halign="center",
        valign="center"
    )
)

# Combine the text with the plate (text() usually creates a separate solid in recent CQ versions 
# that needs to be unioned, but .text() on a workplane often performs the extrusion directly.
# If .text() creates a cut or fails to unite, we might need a different approach, 
# but standard CQ behavior is to add material when distance > 0).

# In standard CadQuery API, .text() creates a solid object on the stack. 
# We need to make sure it's joined to the base.
# The previous chain `recessed_plate...text(...)` creates the text separate from the plate in the variable `result`'s stack.
# We need to explicitly combine them if we want a single object.

# Refined approach to ensure union:
final_text = text_plane.text(
        text_string,
        fontsize=text_size,
        distance=text_thickness,
        font="Serif", 
        halign="center",
        valign="center",
        combine=True # Ensure it fuses with the base
    )

result = final_text