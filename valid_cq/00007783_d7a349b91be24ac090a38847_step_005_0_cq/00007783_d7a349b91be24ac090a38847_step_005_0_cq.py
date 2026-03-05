import cadquery as cq

# -- Parameters --
# Plate dimensions
plate_length = 150.0
plate_width = 30.0
plate_thickness = 3.0
fillet_radius = 2.0  # For the corners of the plate

# Recess/Border dimensions
border_width = 2.0
recess_depth = 1.0  # How deep the "frame" is carved out

# Text parameters
text_string = "Ed Shemanski"
text_size = 12.0
text_thickness = 1.5 # How much the text sticks up from the recessed floor
font_name = "Serif"  # A generic serif font to match the image style

# -- Modeling --

# 1. Base Plate
# Create the main rectangular body
base_plate = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 2. Create the Recess (Frame effect)
# We will cut a pocket into the top face, leaving a border
recess = (
    base_plate.faces(">Z")
    .workplane()
    .rect(plate_length - 2*border_width, plate_width - 2*border_width)
    .cutBlind(-recess_depth)
)

# 3. Add Text
# The text needs to be placed on the floor of the recess.
# Since we cut down by `recess_depth` from the top face (Z = plate_thickness/2),
# the floor is at Z = (plate_thickness/2) - recess_depth.
# However, it's easier to just select the newly created floor face.

# Find the floor of the pocket (it will be the lowest face pointing up)
text_plane = recess.faces(">Z[-2]").workplane() 

# Sometimes face selection by index is brittle, let's target by coordinate if needed, 
# but usually >Z selects the top rim, and the next one down is the floor.
# Alternatively, we can just use center coordinates relative to the original workplane.
# Let's use the safer coordinate method relative to the original Z top.

text_solid = (
    recess.faces(">Z").workplane()  # Start from top face
    .workplane(offset=-recess_depth) # Go down to the floor
    .text(
        text_string,
        fontsize=text_size,
        distance=text_thickness,
        font=font_name,
        halign="center",
        valign="center"
    )
)

# Combine the text with the base plate
result = recess.union(text_solid)

# Optional: Add the small connection tabs/sprue visible on the right side of the image
# It looks like a small frame attached to the side, possibly from injection molding or printing supports.
# I will model a simplified version of this feature.
tab_length = 5.0
tab_width = 12.0
tab_thickness = 2.0

tab_structure = (
    cq.Workplane("XY")
    .box(tab_length, tab_width, tab_thickness)
    .translate((plate_length/2 + tab_length/2, 0, 0)) # Position at the end
)

# Create the internal cutout of the tab to make it look like a frame/ladder
tab_cutout = (
    cq.Workplane("XY")
    .rect(tab_length, tab_width - 2.0)
    .extrude(tab_thickness)
    .translate((plate_length/2 + tab_length/2, 0, -tab_thickness/2))
)

tab_final = tab_structure.cut(tab_cutout)

# Join the tab to the main body
result = result.union(tab_final)

# Export or Render logic is usually handled by the execution environment, 
# but 'result' is the required variable.