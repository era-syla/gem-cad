import cadquery as cq

# --- Object 1: Cylindrical Pin/Stopper ---
# Parametric dimensions for the pin
pin_head_diameter = 20.0
pin_head_height = 15.0
pin_shaft_diameter = 14.0
pin_shaft_height = 15.0
pin_chamfer = 2.0

# Create the shaft
pin_shaft = cq.Workplane("XY").circle(pin_shaft_diameter / 2).extrude(pin_shaft_height)

# Create the head on top of the shaft
pin_head = (
    pin_shaft.faces(">Z")
    .workplane()
    .circle(pin_head_diameter / 2)
    .extrude(pin_head_height)
)

# Apply chamfer to the top edge of the head
pin = pin_head.faces(">Z").edges().chamfer(pin_chamfer)


# --- Object 2: Rectangular Slider/Link ---
# Parametric dimensions for the slider block
block_length = 40.0
block_width = 12.0
block_height = 12.0
hole_diameter = 6.0

# Cutout dimensions
cutout_width = 14.0  # Length of the cutout along the block
cutout_depth = 6.0   # How deep into the block it goes
peg_size = 6.0       # Size of the square peg inside
peg_height = 4.0     # Height of the peg relative to the cutout floor

# Create the main block body
block = cq.Workplane("XY").box(block_length, block_width, block_height)

# Create the longitudinal hole
# We select the face on the X axis (either >X or <X) and drill through
block_with_hole = block.faces(">X").workplane().hole(hole_diameter)

# Create the central cutout
# We select the top face (>Z) and cut a rectangle in the center
block_cut = (
    block_with_hole.faces(">Z")
    .workplane()
    .rect(cutout_width, block_width + 1) # Width + 1 to ensure it cuts through walls
    .cutBlind(-cutout_depth)
)

# Create the square peg inside the cutout
# The peg seems to sit in the center of the cutout. 
# We need to reference the bottom of the cut we just made or calculate the Z level.
# The top face is at Z = block_height/2 = 6.
# The cut floor is at Z = 6 - cutout_depth = 0.
peg = (
    block_cut.faces(">Z[1]") # Select the floor of the cut (often the second highest Z face)
    .workplane()
    .rect(peg_size, peg_size)
    .extrude(peg_height)
)

# Position the slider to the right of the pin so they don't overlap
slider_offset = 50.0
final_slider = peg.translate((slider_offset, 0, 0))

# Combine the objects into a single assembly result
result = pin.union(final_slider)