import cadquery as cq

# Parameters defining the geometry
text_string = "DIVAD"
font_size = 25.0
text_thickness = 8.0   # Depth of the letters (extrusion amount)
base_height = 10.0     # Height of the rectangular base block
base_margin_x = 8.0    # Margin on the left and right of the text
base_margin_y = 6.0    # Margin in front and behind the text

# 1. Create 3D Text
# We create text on the XZ plane so it stands upright relative to the base (XY plane)
# kind="bold" approximates the thick font style in the image
text_model = cq.Workplane("XZ").text(
    text_string, 
    font_size, 
    text_thickness, 
    kind="bold"
)

# 2. Measure the text to size the base
# Access the underlying bounding box of the generated text
bb = text_model.val().BoundingBox()
text_width = bb.xlen
text_height = bb.zlen

# 3. Position the text
# The text is generated centered at (0,0,0) in the XZ plane.
# We need to translate it upwards so its bottom face rests on the top of the base.
# bb.zmin is the lowest Z coordinate of the text. We shift by (base_height - bb.zmin).
z_shift = base_height - bb.zmin
text_model = text_model.translate((0, 0, z_shift))

# 4. Create the Base
# Calculate base dimensions relative to the text size
base_length = text_width + (base_margin_x * 2)
base_depth = text_thickness + (base_margin_y * 2)

# Create a rectangular box for the base.
# It is created on the XY plane and centered.
base = cq.Workplane("XY").box(base_length, base_depth, base_height)

# Move the base up by half its height so its bottom rests at Z=0 and top at Z=base_height
base = base.translate((0, 0, base_height / 2))

# 5. Combine into final result
result = base.union(text_model)