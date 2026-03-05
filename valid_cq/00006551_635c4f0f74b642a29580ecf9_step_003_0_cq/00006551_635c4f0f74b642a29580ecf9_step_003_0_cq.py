import cadquery as cq

# --- Parametric Dimensions ---
# Block dimensions
block_width = 30.0
block_height = 40.0
block_thickness = 20.0
fillet_radius = 2.0

# Pin dimensions
pin_main_dia = 10.0
pin_main_length = 20.0
pin_tip_dia = 6.0
pin_tip_length = 5.0
pin_offset_z = 20.0 # Vertical distance between block top and pin
pin_offset_x = 0.0  # Horizontal alignment

# Hole pattern dimensions on the block
# Top hole (smaller)
hole1_dia = 5.0
hole1_x = -5.0
hole1_y = 5.0

# Middle hole (larger)
hole2_dia = 8.0
hole2_x = 5.0
hole2_y = -2.0

# Bottom slot
slot_width = 12.0 # Total width
slot_height = 6.0
slot_y = -12.0
slot_x = 0.0

# --- Modeling ---

# 1. Create the Main Block
# Create a box centered on XY plane
block = (
    cq.Workplane("XY")
    .box(block_width, block_height, block_thickness)
    .edges("|Z")  # Select vertical edges
    .fillet(fillet_radius)
)

# 2. Cut Features into the Block
# We will sketch on the front face (assumed to be +Z face here based on orientation)
# Note: For clarity in CadQuery's default view, usually XY is "floor", 
# but the image shows the block standing up. Let's orient the block so the holes are on +Y or +Z.
# Let's assume the face with holes is the "Front" (XZ plane typically).

# Re-orienting strategy: Make the block on XY, then rotate or sketch on the appropriate face.
# Let's treat the face with holes as the Top (Z-positive) face for easier sketching coordinates.

# Redefine block logic for easier sketching:
# Let width be X, height be Y, thickness be Z.
base_block = (
    cq.Workplane("XY")
    .box(block_width, block_height, block_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# Cut the top small hole
block_with_holes = (
    base_block.faces(">Z")
    .workplane()
    .pushPoints([(hole1_x, hole1_y)])
    .hole(hole1_dia)
)

# Cut the middle larger hole
block_with_holes = (
    block_with_holes.faces(">Z")
    .workplane()
    .pushPoints([(hole2_x, hole2_y)])
    .hole(hole2_dia)
)

# Cut the bottom slot
block_with_holes = (
    block_with_holes.faces(">Z")
    .workplane()
    .center(slot_x, slot_y)
    .slot2D(length=slot_width, diameter=slot_height, angle=0)
    .cutBlind(-block_thickness) # Cut all the way through
)

# Rotate the block so it stands upright (Face with holes facing +Y)
# Currently holes are on +Z. Rotate 90 deg around X.
final_block = block_with_holes.rotate((0,0,0), (1,0,0), 90)


# 3. Create the Pin (Cylinder with a step)
# Let's create it along the Y axis to match the block's orientation in the image
pin = (
    cq.Workplane("XZ") # Start on XZ plane to extrude along Y
    .circle(pin_main_dia / 2)
    .extrude(pin_main_length)
    .faces(">Y")
    .workplane()
    .circle(pin_tip_dia / 2)
    .extrude(pin_tip_length)
)

# Move the pin to position above the block
# The block is centered at origin.
# Block top is at Z = block_height/2 (20).
# We want the pin above that.
pin_moved = pin.translate((pin_offset_x, 0, block_height/2 + pin_offset_z))
# The pin in the image is angled slightly, but typical CAD representation keeps parts aligned.
# Based on the isometric view, the pin is just floating above.

# 4. Combine into final result
result = final_block.union(pin_moved)