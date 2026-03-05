import cadquery as cq

# Parameters
text_string = "EXAMPLE TEXT"
text_size = 10.0      # Font size height
text_thickness = 5.0  # Extrusion depth of the text
block_size = 20.0     # Dimensions of the cube
hole_diameter = 8.0   # Diameter of the hole in the block
spacing = 2.0         # Gap between text and block

# 1. Create the 3D Text
# We create text on the XY plane and extrude it.
# Usually, CadQuery's text() creates 2D wire/face which we then extrude.
text_obj = (
    cq.Workplane("XY")
    .text(text_string, fontsize=text_size, distance=text_thickness)
)

# 2. Create the Mounting Block
# We need to position the block relative to the text.
# The text is centered by default. We need to find its bounding box to position the block correctly.
# However, text bounding boxes can be tricky. A parametric approach estimates the length.
# Alternatively, we can just build the block at a specific offset.
# Let's assume the text ends at some X coordinate and place the block to the right.
# An average character width is often ~0.6 * size.
estimated_text_length = len(text_string) * (text_size * 0.7) 
block_center_x = (estimated_text_length / 2) + (block_size / 2) + spacing

# Create the cube
block = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start at z=0 to align with text bottom
    .box(block_size, block_size, block_size, centered=(True, True, False))
)

# Create the hole
block = (
    block.faces(">Y")
    .workplane()
    .hole(hole_diameter)
)

# Move the block to the end of the text
# Since we don't know the exact bounding box of the text without computing it,
# we will construct the text first, measure it (conceptually), or just move it manually 
# based on the visual evidence.
# In the image, the block is to the right of the text.
# Let's shift the block.
# Note: CadQuery text is centered at (0,0).
# Let's try to get the bounding box of the text to be precise.
text_bb = text_obj.val().BoundingBox()
text_max_x = text_bb.xmax

# Position block slightly to the right of the text's maximum X extent
block_x_pos = text_max_x + (block_size / 2) + spacing
# The text in the image looks like it sits on the "floor" (Z=0) or is centered. 
# The block is a cube.
# Let's move the block to the correct X position.
block = block.translate((block_x_pos, 0, (text_thickness - block_size)/2)) 
# Adjust Z: The image shows the text roughly centered vertically on the block or aligned.
# Let's align the bottom of the text with the bottom of the block for stability, or center them.
# In the image, the text thickness (Z) is less than the block. The text seems "standing up".
# Let's re-orient. The image shows text standing on the X-Y plane (extruded in Z).
# The block is to the right.
# Let's adjust the Z translation of the block to make it look like the image.
# If text is extruded 5mm in Z, and block is 20mm in Z.
# Let's move the block so its bottom is at Z=0.
block = (
    cq.Workplane("XY")
    .box(block_size, block_size, block_size, centered=(True, True, False)) # Box sits on Z=0
    .translate((block_x_pos, 0, 0))
    .faces(">Y").workplane().center(0, block_size/2).hole(hole_diameter) # Hole in the middle of the face
)

# 3. Combine parts
result = text_obj.union(block)

# Optional: Rotate for better viewing angle similar to image
result = result.rotate((0,0,0), (1,0,0), -90) # Flip up so text reads correctly from front view
result = result.rotate((0,0,0), (0,0,1), -45) # Angle it