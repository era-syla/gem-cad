import cadquery as cq

# Parametric dimensions
base_length = 80.0
base_width = 30.0
base_thickness = 5.0

block_length = 25.0  # Length of the raised blocks
block_width = 25.0   # Width of the raised blocks
block_height = 15.0  # Height from the TOP of the base plate (total height = base + block)
                     # Or height of the block itself. Let's assume height of block above base.

hole_diameter = 6.0

# Calculate the center position for the blocks relative to the ends
# Let's align them flush with the ends based on the image visual
# Block 1 is on the left, Block 2 is on the right.

# Step 1: Create the Base Plate
# We start with a simple rectangular box centered on XY
result = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# Step 2: Create the Left Block
# We position a workplane on top of the base
# The block looks like it is flush with the left end and the sides
left_block_center_x = -base_length/2 + block_length/2
# The image shows the block width is slightly less than base width or equal?
# Looking closely, the blocks seem slightly narrower than the base, leaving a small lip.
# Or maybe they are flush? Let's assume a slight margin for a more realistic mechanical part look,
# or create them centered.
# Re-evaluating image: The blocks look square. The base is rectangular. 
# The blocks are centered along the Y-axis. 
# The block on the left is flush with the left edge. The block on the right is flush with the right edge.
# Let's use `union` to add them.

# Redefining block position strategy:
# Create a sketch on the top face of the base
result = result.faces(">Z").workplane() \
    .pushPoints([
        (-base_length/2 + block_length/2, 0),  # Center for left block
        (base_length/2 - block_length/2, 0)    # Center for right block
    ]) \
    .rect(block_length, block_width) \
    .extrude(block_height)

# Step 3: Create the Center Hole
# The hole is in the exact center of the base
# We select the top face of the base (between the blocks) or just use the XY plane and cut through
result = result.faces(">Z").workplane().center(0, 0).circle(hole_diameter/2).cutThruAll()

# If we want to be very precise about the "cutThruAll" originating from the right height,
# selecting the top face of the base plate (z = base_thickness) is safer than the top of the blocks.
# The previous chain ended with extrude, so the active workplane is on top of the blocks.
# Let's reset to the base top face for the hole operation to be clean.

result = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_thickness)
    .faces(">Z").workplane()
    .pushPoints([
        (-base_length/2 + block_length/2, 0),
        (base_length/2 - block_length/2, 0)
    ])
    .rect(block_length, block_width)
    .extrude(block_height)
    .faces("<Z").workplane() # Go to bottom face
    .center(0, 0)
    .circle(hole_diameter/2)
    .cutThruAll()
)