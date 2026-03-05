import cadquery as cq

# -- Parameters --
# Main block dimensions
block_width = 100.0  # Width (X direction)
block_depth = 60.0   # Depth (Y direction)
block_height = 80.0  # Height (Z direction)

# Step cutout dimensions
step_width = 30.0    # How wide the cut is (X direction)
step_depth_offset = 5.0 # How much the top plate overhangs or the depth difference

# Top Plate dimensions
plate_thickness = 2.0
plate_width = step_width
plate_depth = block_depth

# Hole parameters
hole_diameter = 2.5
hole_spacing = 15.0  # Distance between holes
# Position of the first hole relative to the corner
hole_start_x = -block_width/2 + step_width/2 
hole_start_y = block_depth/2 - 10.0

# -- Modeling --

# 1. Create the main base block
# We start with a full block
base = cq.Workplane("XY").box(block_width, block_depth, block_height)

# 2. Create the step (cutout)
# We want to remove material from the left side (negative X) to create the lower section.
# However, looking closely at the image, it looks like two joined blocks or a block with a side extension.
# Let's model it as the main large block on the right, and the thinner, separate-looking tall block on the left.
# Actually, looking at the seamless vertical line, it looks like a single assembly or a complex extrusion. 
# Let's try a subtractive approach which is often robust.

# Let's redefine based on the visual features:
# Feature A: Large block on the right.
# Feature B: Thinner block on the left, slightly set back or flush?
# Looking at the "step", there is a vertical face separating the left part and right part.
# The left part has a top plate.

# Let's try an additive approach for clarity.
# Right Block (Main body)
right_block_width = block_width - step_width
right_block = cq.Workplane("XY").box(right_block_width, block_depth, block_height)
# Move it to the right position
right_block = right_block.translate((step_width/2, 0, 0))

# Left Block (The narrower part)
# It seems to be the same height as the right block but has a plate on top? 
# No, looking closely, the left part is slightly lower, and then a plate is added on top to make it flush or slightly higher?
# Actually, the image shows a continuous vertical surface on the front-left, but there is a seam line on top.
# The plate on the left is distinct.
# Let's assume the left underlying block is shorter by the plate thickness.

left_block_height = block_height - plate_thickness
left_block = cq.Workplane("XY").box(step_width, block_depth, left_block_height)
# Move it to the left position and down to align bottom
left_block = left_block.translate((-right_block_width/2, 0, -plate_thickness/2))

# Combine the two solid blocks
main_body = right_block.union(left_block)

# 3. Create the Top Plate
# The plate sits on top of the left block.
plate = cq.Workplane("XY").box(step_width, block_depth, plate_thickness)
# Position it on top of the left block
plate_z_pos = (left_block_height/2) + (plate_thickness/2) - (plate_thickness/2) # adjusting for center-based positioning
# Actually simpler: The top of left block is at Z = (block_height/2) - plate_thickness
# The plate center Z needs to be at (block_height/2) - (plate_thickness/2)
plate = plate.translate((-right_block_width/2, 0, (block_height/2) - (plate_thickness/2)))

# 4. Add holes to the plate
# The image shows holes along the top edge of the plate/left side.
# There appear to be 2 holes visible on the left plate part, and maybe holes continuing on the right?
# Let's look closer. There are two holes on the separate plate (left) and two holes on the main block (right) that seem aligned.
# Or is it a single plate covering the left part?
# The image shows a seam. The left part is a separate cover.
# There are two holes on the rear of the left plate.
# There are two holes on the rear of the right block top surface.

# Let's add holes to the plate first.
plate_with_holes = (
    plate.faces(">Z").workplane()
    .pushPoints([
        (0, block_depth/2 - 5.0),    # Near back edge
        (0, block_depth/2 - 15.0),   # Slightly forward
    ])
    .hole(hole_diameter)
)

# 5. Add holes to the main block top
# They seem to align with the plate holes in Y, but are shifted in X.
main_body_with_holes = (
    main_body.faces(">Z").workplane()
    # Let's pick points relative to the top face center of the right block
    # The right block width is right_block_width. Center is at X = step_width/2 relative to global origin.
    # We want holes near the seam.
    .pushPoints([
        (-right_block_width/2 + 5.0, block_depth/2 - 5.0),   # Near seam and back
        (-right_block_width/2 + 15.0, block_depth/2 - 5.0)  # Further right
    ])
    .hole(hole_diameter)
)

# Combine everything
# Note: The 'plate' sits on the 'left_block' which is part of 'main_body'.
result = main_body_with_holes.union(plate_with_holes)

# Re-evaluating the image visually:
# The vertical line on the front face suggests the left part is a separate extrusion or assembly.
# The top left surface is a thin plate.
# There are holes on the *back* edge.
# Left plate: 2 holes.
# Right block top: 2 holes near the seam.

# Let's refine the hole positions to match the image better.
# The image shows the back-left corner having holes.
# On the left plate: 2 holes along the Y axis near the back.
# On the right block: 2 holes along the X axis near the back seam.

# Clean up hole generation logic for the final script
result = result.faces(">Z[1]").workplane().pushPoints([(0, 0)]).hole(0.1) # Dummy operation to reset context if needed, but not strictly necessary with fresh workplanes.

# Let's rebuild the hole logic cleanly on the final union to ensure consistency
# It's easier to subtract holes from the final union if we know coordinates.

# Final Geometry Construction
# 1. Right Block
solid_right = cq.Workplane("XY").box(70, 60, 80).translate((15, 0, 0))

# 2. Left Block (lower base for plate)
solid_left_base = cq.Workplane("XY").box(30, 60, 78).translate((-35, 0, -1))

# 3. Left Plate
plate_solid = cq.Workplane("XY").box(30, 60, 2).translate((-35, 0, 39))

# Union them
result = solid_right.union(solid_left_base).union(plate_solid)

# Add holes
# Holes on the left plate (Top face at Z=40)
# Looking at image: Top left corner (backwards in standard CAD view usually)
# Let's assume Back is +Y.
result = (
    result.faces(">Z")
    .workplane()
    # Holes on the left strip (the plate)
    # Center of left strip is X = -35. Back edge is Y=30.
    .pushPoints([
        (-35, 25), # Back-most hole on plate
        (-35, 15)  # Second hole on plate
    ])
    .hole(2.5)
)

# Holes on the right block (Top face at Z=40)
result = (
    result.faces(">Z")
    .workplane()
    # Holes on the right block, near the seam.
    # Seam is at X = -20. Back edge is Y=30.
    .pushPoints([
        (-10, 25), # Hole to the right of the seam
        (5, 25)    # Further right
    ])
    .hole(2.5)
)