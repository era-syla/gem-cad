import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
block_height = 60.0
block_width = 50.0
block_depth = 25.0

# Large central hole
main_bore_diameter = 30.0
main_bore_center_y = block_height / 2.0  # Centered vertically relative to the block height? 
                                         # Looking at the image, it seems slightly lower than center, 
                                         # but centered is a safe parametric default. 
                                         # Let's approximate it as slightly offset downwards based on typical part design.
main_bore_offset_from_bottom = 25.0 # Distance from bottom edge to center

# Top slot dimensions
slot_width = 15.0
slot_depth = 10.0

# Small front face hole (top right)
small_hole_diameter = 3.0
# Position relative to top-right corner or center
small_hole_offset_x = 10.0 # From center to right
small_hole_offset_y = 15.0 # From center to top

# Side hole (bottom left)
side_hole_diameter = 6.0
side_hole_z_pos = 10.0 # Height from bottom

# --- Geometry Construction ---

# 1. Start with the main rectangular block
# We center it on X and Y to make symmetry operations easier, but Z starts at 0
result = cq.Workplane("XY").box(block_width, block_height, block_depth)

# 2. Cut the large central bore
# The bore goes through the thickness (Z-axis relative to our initial box orientation, 
# but visually it's the Y-axis if we consider the image front face as XY)
# Let's adjust the orientation to match the image:
# Front face is X-Z plane in standard engineering view, or X-Y in CadQuery default workplane.
# Let's stick to the default Workplane("XY") being the front face shown in the image.
# So thickness is Z.

# Create the main block
result = cq.Workplane("XY").box(block_width, block_height, block_depth)

# Cut the large central hole
# Based on image, the hole is roughly centered horizontally, but vertically offset.
result = result.faces(">Z").workplane().center(0, -5).hole(main_bore_diameter)
# Note: box is centered at (0,0,0). Height is 60. Center is 0. 
# "offset from bottom 25" means -30 (bottom) + 25 = -5.

# 3. Cut the top slot
# The slot is on the top face (+Y face), running along the depth (Z).
# It looks offset to the right side of the part.
slot_x_center = (block_width / 2.0) - (slot_width / 2.0) # Aligned to right edge? 
# Looking closer, it looks like a notch on the top right corner.
# Let's assume it's a centered slot or a corner notch. 
# Re-evaluating image: It looks like a notch on the top edge, slightly offset to the right.
# Let's model it as a cutout on the top face (+Y).
result = result.faces(">Y").workplane().center(block_width/4.0, 0).rect(slot_width, block_depth).cutThruAll()

# 4. Cut the small hole on the front face
# Located top-right relative to the big hole.
# Front face is >Z (top of the extrusion) or <Z depending on view.
# Let's use >Z face.
# Position: X positive (right), Y positive (up).
result = result.faces(">Z").workplane().center(15, 20).hole(small_hole_diameter, depth=10) # Blind hole presumably

# 5. Cut the side hole (bottom left side)
# This is on the -X face (left face).
# Position is near the bottom.
# Z-height in 3D space corresponds to Y in our 2D workplane logic for the side face.
result = result.faces("<X").workplane().center(0, -block_height/2.0 + side_hole_z_pos).hole(side_hole_diameter)

# Refinement on dimensions based on visual proportions
# Let's rebuild with a more cleaner approach using a single chain if possible or step-by-step
# to ensure the coordinates are logical.

# --- Revised Construction ---

length = 50.0  # X
height = 60.0  # Y
thickness = 20.0 # Z

# Main Body
result = cq.Workplane("XY").box(length, height, thickness)

# 1. Large Central Hole
# Visually, it looks centered in X, slightly below center in Y.
large_hole_dia = 32.0
large_hole_y_offset = -5.0 
result = result.faces(">Z").workplane().center(0, large_hole_y_offset).hole(large_hole_dia)

# 2. Top Slot
# On the top edge (+Y), offset to the right (+X).
slot_w = 12.0
slot_d = 8.0 # Depth into the Y axis
# To cut this, we select the top face (>Y)
# The local X is global X. The local Y is global Z (thickness).
result = result.faces(">Y").workplane().center(10, 0).rect(slot_w, thickness).cutBlind(-slot_d)

# 3. Small Front Hole
# Top right quadrant.
small_hole_dia = 4.0
# Coordinates relative to center of front face
small_hole_x = 15.0
small_hole_y = 20.0 
result = result.faces(">Z").workplane().center(small_hole_x, small_hole_y).hole(small_hole_dia)

# 4. Side Hole
# Bottom of the left face (-X).
side_hole_dia = 8.0
# Select left face. Local X is global Y. Local Y is global Z.
# Actually, workplane orientation on faces can be tricky.
# Let's specify explicitly.
# We want a hole running through the X axis, located at bottom.
side_hole_height_from_bottom = 10.0
y_pos_side_hole = -height/2.0 + side_hole_height_from_bottom
result = result.faces("<X").workplane(centerOption="CenterOfMass") \
    .center(0, y_pos_side_hole) \
    .hole(side_hole_dia) # This might misalign if local axes are rotated.

# Alternative safer way for side hole:
# Select Left face (<X). 
# Default axes: X moves along global Y, Y moves along global Z.
# We want to move along global Y (to the bottom).
result = result.faces("<X").workplane().center(-20, 0).hole(side_hole_dia) 
# center(-20, 0): -20 along local X (global Y down), 0 along local Y (global Z center)

# Final check of the generated code logic
final_block = cq.Workplane("XY").box(50, 60, 25) \
    .faces(">Z").workplane().center(0, -5).hole(30) \
    .faces(">Y").workplane().center(12, 0).rect(15, 25).cutBlind(-10) \
    .faces(">Z").workplane().center(18, 22).hole(4) \
    .faces("<X").workplane().center(-20, 0).hole(8)

result = final_block