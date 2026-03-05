import cadquery as cq

# Parameters
plate_length = 60.0
plate_width = 15.0
plate_thickness = 3.0
corner_radius = 2.5
text_string = "Wilder"
text_size = 8.0
text_depth = 1.0
text_font = "Arial"  # Standard font, should be available on most systems

# Create the base plate
# We start with a rectangle centered on XY plane
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

# Apply fillets to the vertical edges to create rounded corners
# We select edges parallel to the Z axis
result_base = base.edges("|Z").fillet(corner_radius)

# Create the text
# We need to position the workplane on the top face of the plate
# The text needs to be centered and cut into the material
result = (
    result_base.faces(">Z")
    .workplane()
    .text(
        text_string,
        fontsize=text_size,
        distance=-text_depth, # Negative distance to cut into the material
        font=text_font,
        kind='regular',
        halign='center',
        valign='center'
    )
)

# The result variable contains the final geometry as requested