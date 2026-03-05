import cadquery as cq

# --- Parameters ---
# Back block dimensions
back_length = 35.0
back_width = 45.0
back_height = 30.0
back_hole_dia = 12.0

# Front plate dimensions
front_length = 55.0   # Length extending from the back block face
front_width = 35.0    # Slightly narrower to create the step feature on the side
front_height = 15.0
front_hole_dia = 5.0
front_hole_spacing_x = 20.0
front_hole_spacing_y = 18.0

# --- Modeling ---

# 1. Create the Back Block
# Aligned such that the bottom face is on the XY plane (Z=0)
# and centered in X and Y.
back_block = cq.Workplane("XY").box(back_length, back_width, back_height, centered=(True, True, False))

# 2. Create the Front Plate (before rounding)
# Calculate the center position for the front plate to ensure it starts exactly at the face of the back block
# Front face of back block is at x = back_length / 2
front_center_x = (back_length / 2.0) + (front_length / 2.0)

front_plate = (
    cq.Workplane("XY")
    .workplane(offset=0)  # Start at bottom (flush with back block)
    .moveTo(front_center_x, 0)
    .rect(front_length, front_width)
    .extrude(front_height)
)

# 3. Union the two parts
result = back_block.union(front_plate)

# 4. Apply Full Fillet to the front end
# Select the vertical edges at the furthest positive X coordinate
result = result.edges(">X and |Z").fillet(front_width / 2.0 - 0.001)

# 5. Cut the hole in the Back Block
# Select the highest face (top of back block)
result = (
    result.faces(">Z")
    .workplane()
    .hole(back_hole_dia)
)

# 6. Cut the 4 holes in the Front Plate
# We need to select the top face of the front section. 
# We use a selector to find the face with normal +Z that is nearest to the center of the front plate.
target_point = (front_center_x, 0, front_height)
result = (
    result.faces("+Z")
    .faces(cq.NearestToPointSelector(target_point))
    .workplane()
    # Create a rectangular pattern for the holes
    .rect(front_hole_spacing_x, front_hole_spacing_y, forConstruction=True)
    .vertices()
    .hole(front_hole_dia)
)

# The 'result' variable now contains the final solid geometry.