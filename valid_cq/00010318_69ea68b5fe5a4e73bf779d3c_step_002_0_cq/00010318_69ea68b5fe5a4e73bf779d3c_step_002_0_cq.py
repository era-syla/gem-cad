import cadquery as cq

# --- Parameter Definitions ---

# Main body dimensions
length = 80.0
width = 30.0
height = 15.0
wall_thickness = 2.0
fillet_radius = 15.0  # Radius for the rounded end

# Internal cavity
cavity_depth = height - wall_thickness  # Keep bottom or top thickness

# USB Port cutout dimensions (approximate standard USB-A)
usb_width = 14.0
usb_height = 7.0
port_spacing = 35.0 # Distance between centers of the two recessed areas

# Recessed area on the front face
recess_depth = 2.0
recess_width = 25.0
recess_height = 10.0
recess_spacing = 30.0 # spacing between the two recessed zones

# Internal mounting features (bosses/standoffs visible in the cutout)
boss_height = 5.0
boss_width = 4.0
boss_depth = 4.0

# Top holes (screw holes)
hole_diameter = 2.5
hole_locations = [(-30, 0), (0, 0), (25, 10)] # Approximate positions relative to center

# Text parameters
text_string = "USB"
text_size = 8.0
text_depth = 0.5

# --- Geometry Construction ---

# 1. Base Shape: Rectangle with one rounded corner
# Create a 2D sketch for the profile
base_sk = (
    cq.Sketch()
    .rect(length, width)
    .vertices(">X") # Select vertices on the positive X side
    .fillet(fillet_radius)
)

# Extrude the base shape
base = cq.Workplane("XY").placeSketch(base_sk).extrude(height)

# 2. Hollow out the inside (creating a shell)
# We will shell from the bottom or back, but based on the image, 
# it looks like a solid block with specific cutouts. 
# Let's model it as a solid first, then cut into it.

# 3. Create the Front Recesses
# The image shows two rectangular recessed areas on the front face (-Y face)
# We need to position workplane on the front face.

front_face = base.faces("<Y").workplane()

# Create the left recess
left_recess = (
    front_face
    .center(-length/4 + 5, 0) # Shift to left side
    .rect(recess_width, recess_height)
    .cutBlind(-recess_depth)
)

# Create the right recess (which goes deeper/through for the connector)
# The right side has a deeper cutout structure.
right_cutout_center_x = length/4
right_cutout_width = 28.0
right_cutout_height = 12.0
right_cutout_depth = 10.0 # Deeper

# Cut the right main cavity
base_with_left = left_recess
base_with_cavities = (
    base_with_left.faces("<Y").workplane()
    .center(right_cutout_center_x, 0)
    .rect(right_cutout_width, right_cutout_height)
    .cutBlind(-right_cutout_depth)
)

# 4. Add Internal Details to Right Cavity (The "USB" port look)
# There is a block inside the right cavity.
internal_block = (
    base_with_cavities.faces("<Y").workplane()
    .center(right_cutout_center_x, 0) # Same center
    .rect(12, 6) # Smaller block (the connector tongue)
    .extrude(right_cutout_depth - 2) # Extrude back out towards front, but not flush
)

# Add side supports inside the right cavity (as seen in image)
# Left support
support_l = (
    base_with_cavities.faces("<Y").workplane()
    .center(right_cutout_center_x - 10, 0)
    .rect(4, right_cutout_height)
    .extrude(right_cutout_depth - 4)
)
# Right support
support_r = (
    base_with_cavities.faces("<Y").workplane()
    .center(right_cutout_center_x + 10, 0)
    .rect(4, right_cutout_height)
    .extrude(right_cutout_depth - 4)
)

# Combine supports and block
result_geo = internal_block.union(support_l).union(support_r)


# 5. Add Text "USB" on Top
# We need to orient and position the text correctly.
# The text is along the length, rotated 90 degrees or upright relative to the view.
# Looking at image: "U" is towards left, "B" towards middle.

# Create text workplane on top face
text_wp = result_geo.faces(">Z").workplane()

# Cut the text
# Position: roughly centered on the left half
result_with_text = (
    text_wp
    .center(-15, -5) # Adjust position
    .text(text_string, text_size, -text_depth, font="Arial", kind='regular', halign='center', valign='center')
)

# 6. Add Screw Holes
# There are 3 visible holes on the top face
# 1. Top left corner
# 2. Middle (near the text)
# 3. Top right (in the curved area)

hole_1_pos = (-length/2 + 8, width/2 - 6)
hole_2_pos = (-5, width/2 - 6)
hole_3_pos = (length/2 - 12, width/2 - 8) # On the curve

final_model = (
    result_with_text.faces(">Z").workplane()
    .pushPoints([hole_1_pos, hole_2_pos, hole_3_pos])
    .hole(hole_diameter)
)

# 7. Add small holes inside the right connector area (mounting holes for the component)
# Visible inside the right cavity on the little side supports
side_hole_z_offset = 0 # vertically centered
side_hole_x_offset_l = right_cutout_center_x - 10
side_hole_x_offset_r = right_cutout_center_x + 10

# To drill these horizontally, we select the face inside the cutout
# It's easier to just drill from the front face all the way through the supports
final_model = (
    final_model.faces("<Y").workplane()
    .pushPoints([
        (side_hole_x_offset_l, 0), 
        (side_hole_x_offset_r, 0)
    ])
    .hole(1.5, depth=right_cutout_depth) # Small screw holes
)

# Assign to result variable
result = final_model