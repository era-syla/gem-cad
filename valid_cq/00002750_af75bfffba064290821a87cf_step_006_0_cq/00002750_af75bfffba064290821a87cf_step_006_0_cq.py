import cadquery as cq

# Parametric dimensions
main_length = 50.0
main_width = 30.0
main_height = 10.0

cutout_width = 15.0
cutout_length = 15.0  # Length of the stepped section removed

pin_diameter = 8.0
pin_length = 10.0

# 1. Create the main rectangular body
base_block = cq.Workplane("XY").box(main_length, main_width, main_height)

# 2. Create the L-shaped cutout (step) on one corner
# We'll select the top face, draw a rectangle at the corner, and cut down
result_with_cutout = (
    base_block.faces(">Z")
    .workplane()
    .rect(cutout_length, cutout_width, centered=False)
    # Positioning the rectangle to cut the specific corner visible in the image
    # Assuming origin is center, we move it to a corner
    .translate((main_length/2 - cutout_length, -main_width/2))
    .cutBlind(-main_height)
)

# 3. Add the cylindrical pin
# The pin protrudes from the front face of the remaining section next to the cutout
result = (
    result_with_cutout.faces(">X")  # Select the front-most face
    .workplane()
    # Shift the workplane center to align with the non-cutout part
    .center(0, main_width/4) 
    .circle(pin_diameter / 2)
    .extrude(pin_length)
)

# To ensure the pin is on the correct side relative to the cut (based on visual inspection):
# The previous logic placed the cut on X+, Y- corner. 
# The pin is on the X+ face, but shifted towards Y+.
# Let's refine the construction for clarity and robustness.

# Alternative Construction Strategy: Additive approach
# Part A: The larger rectangular section
part_a_width = main_width - cutout_width
part_a = cq.Workplane("XY").box(main_length, part_a_width, main_height, centered=(True, True, True))

# Part B: The shorter rectangular section (the "L" shape extension)
part_b_length = main_length - cutout_length
part_b = (
    cq.Workplane("XY")
    .box(part_b_length, cutout_width, main_height, centered=(True, True, True))
    .translate((-cutout_length/2, -(part_a_width/2 + cutout_width/2), 0)) # Move next to Part A
)

# Combine A and B
body = part_a.union(part_b)

# Part C: The pin
# The pin comes out of the X+ face of Part A
pin = (
    cq.Workplane("YZ")
    .circle(pin_diameter / 2)
    .extrude(pin_length)
    .translate((main_length/2, 0, 0)) # Position at end of Part A
)

result = body.union(pin)