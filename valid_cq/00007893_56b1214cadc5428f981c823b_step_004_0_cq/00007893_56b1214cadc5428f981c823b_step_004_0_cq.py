import cadquery as cq

# Parametric dimensions
# Main tall block dimensions
main_width = 40.0   # Width (along X)
main_depth = 40.0   # Depth (along Y)
main_height = 80.0  # Height (along Z)

# Side short block dimensions
side_width = 20.0   # How far it sticks out (along X)
side_depth = 40.0   # Depth (along Y, same as main block usually)
side_height = 40.0  # Height (along Z)

# Create the main tall block
# Centered on X and Y, base at Z=0 for convenience
main_block = cq.Workplane("XY").box(main_width, main_depth, main_height, centered=(True, True, False))

# Create the side short block
# We want to attach this to the side of the main block.
# Let's calculate the center position for the side block.
# X position: needs to be shifted by half of main_width + half of side_width to touch the face.
# However, looking at the image, the blocks seem to share a face or be an L-shape.
# Let's position the side block relative to the main block.
# We will shift it in -X direction relative to the main block.
side_x_pos = -(main_width / 2.0) - (side_width / 2.0)

# Create the side block geometry
side_block = (
    cq.Workplane("XY")
    .center(side_x_pos, 0) # Shift center in X
    .box(side_width, side_depth, side_height, centered=(True, True, False))
)

# Combine the two blocks into a single solid
result = main_block.union(side_block)

# Export or display result (for verification purposes in environment, though typically 'result' variable is enough)
# cq.exporters.export(result, "result.step")