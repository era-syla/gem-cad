import cadquery as cq

# --- Parameters ---
# Main body dimensions
block_length = 60.0
block_width = 30.0
block_height = 30.0

# Front cutout/recess dimensions
recess_depth = 20.0  # Depth of the U-shaped cutout from the front
recess_width = 18.0  # Width of the cutout
recess_height_from_top = 15.0 # How deep the cutout goes from the top face

# Front tube dimensions
tube_outer_dia = 10.0
tube_inner_dia = 7.0
tube_length = 15.0 # Length protruding from the front face
tube_pos_z = 10.0  # Height of the tube center from the bottom

# Internal bore (hole through the front face below the recess)
bore_dia = 12.0
bore_depth = 20.0 # How deep into the block the hole goes

# Top slot dimensions
slot_length = 20.0
slot_width = 3.0
slot_depth = 5.0
slot_offset_x = 10.0 # Offset from the center or reference point

# --- Modeling ---

# 1. Create the main rectangular block
main_body = cq.Workplane("XY").box(block_length, block_width, block_height)

# 2. Create the U-shaped cutout on the top-front
# We'll sketch on the front face and cut back
cutout = (
    cq.Workplane("YZ")
    .workplane(offset=-block_length/2.0) # Move to front face
    .center(0, block_height/2.0)         # Move to top edge center
    .rect(recess_width, recess_height_from_top * 2) # Draw rect centered on edge
    .extrude(recess_depth)               # Extrude into the body
)
# The cutout is currently a separate solid, let's subtract it later or cut directly.
# Let's rewrite using the main body context to cut directly.

result = main_body.faces(">X").workplane().center(0, block_height/2 - recess_height_from_top/2).rect(recess_width, recess_height_from_top).cutBlind(-recess_depth)

# 3. Create the circular bore on the front face (below the cutout)
# This looks like the housing for the tube, or just a lower hole.
# Based on the image, the tube connects into a hole.
# Let's align it with the tube position.
result = result.faces(">X").workplane().center(0, tube_pos_z - block_height/2).circle(bore_dia/2).cutBlind(-bore_depth)


# 4. Create the protruding tube
# We create a cylinder and join it.
tube = (
    cq.Workplane("YZ")
    .workplane(offset=block_length/2.0) # Front face
    .center(0, tube_pos_z - block_height/2)
    .circle(tube_outer_dia/2)
    .circle(tube_inner_dia/2)
    .extrude(tube_length)
)

result = result.union(tube)

# 5. Create the slot on the top face
# The slot is located behind the cutout.
slot_center_x = (block_length/2) - recess_depth - (slot_length/2) - 5.0 # Approximate position
result = result.faces(">Z").workplane().center(-10, 0).slot2D(slot_length, slot_width).cutBlind(-slot_depth)


# Refine the front U-shaped cutout to have a rounded back if needed.
# The image shows a flat U-shape bottom, but possibly a rounded transition at the back?
# Looking closely at the image, the cutout on top has a rounded back wall (vertical cylinder cut).
# Let's redo step 2 to be more accurate to the image.

# Reset and rebuild with a cleaner sequence
# 1. Main Block
res = cq.Workplane("XY").box(block_length, block_width, block_height)

# 2. Top-Front Recess (U-shape with rounded back)
# We will cut a rectangle from the front, then a cylinder vertically to round the back
recess_rect_cut = (
    cq.Workplane("XY")
    .workplane(offset=block_height/2) # Top face
    .center(block_length/2 - recess_depth/2, 0)
    .rect(recess_depth, recess_width)
    .extrude(-recess_height_from_top, combine=False)
)
# We need to shift this cut to the edge properly
recess_rect_cut = recess_rect_cut.translate((0,0,0)) # Placeholder

# Let's try a different approach: Cut the rectangular part from the front face
res = res.faces(">X").workplane().center(0, (block_height/2) - (recess_height_from_top/2)).rect(recess_width, recess_height_from_top).cutBlind(-recess_depth)

# Now round the back of that cut. It looks like a vertical hole at the end of the recess.
res = res.faces(">Z").workplane().center((block_length/2) - recess_depth, 0).circle(recess_width/2).cutBlind(-recess_height_from_top)


# 3. Lower Front Hole (Main bore)
res = res.faces(">X").workplane().center(0, tube_pos_z - block_height/2).circle(bore_dia/2).cutBlind(-recess_depth)

# 4. The Tube
# The tube sticks out from the front face, aligned with the hole we just made, but likely smaller diameter
tube_geo = (
    cq.Workplane("YZ")
    .workplane(offset=block_length/2) # Front face plane
    .center(0, tube_pos_z - block_height/2)
    .circle(tube_outer_dia/2)
    .circle(tube_inner_dia/2)
    .extrude(tube_length)
)
res = res.union(tube_geo)


# 5. Top Slot
# Position it behind the recess
res = res.faces(">Z").workplane().center(-5, 0).slot2D(slot_length, slot_width).cutBlind(-slot_depth)

result = res