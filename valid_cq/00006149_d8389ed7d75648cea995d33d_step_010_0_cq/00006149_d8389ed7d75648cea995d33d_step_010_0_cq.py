import cadquery as cq

# --- Parametric Dimensions ---
# Block dimensions
block_length = 100.0
block_width = 50.0
block_height = 50.0

# Small holes (group of 4 on the top left)
small_hole_diameter = 6.0
small_hole_depth = 15.0  # Assumed blind holes based on image
small_hole_spacing_x = 15.0
small_hole_spacing_y = 30.0
small_hole_group_offset_x = -30.0 # Shifted towards the left end

# Large central top hole
large_hole_diameter = 14.0
large_hole_depth = 25.0
large_hole_offset_x = 15.0 # Shifted towards the right from center

# End face hole
end_hole_diameter = 8.0
end_hole_depth = 30.0

# --- Modeling ---

# 1. Create the base block
result = cq.Workplane("XY").box(block_length, block_width, block_height)

# 2. Add the four small holes on the top face
# We select the top face
result = (result.faces(">Z").workplane()
          # Move to the center of the group of holes
          .center(small_hole_group_offset_x, 0)
          # Create a rectangular pattern for the 4 holes
          .rect(small_hole_spacing_x, small_hole_spacing_y, forConstruction=True)
          .vertices()
          .hole(small_hole_diameter, small_hole_depth))

# 3. Add the single large hole on the top face
result = (result.faces(">Z").workplane()
          .center(large_hole_offset_x, 0)
          .hole(large_hole_diameter, large_hole_depth))

# 4. Add the hole on the end face (visible right side in image)
result = (result.faces(">X").workplane()
          .center(0, 0) # Center of the face
          .hole(end_hole_diameter, end_hole_depth))