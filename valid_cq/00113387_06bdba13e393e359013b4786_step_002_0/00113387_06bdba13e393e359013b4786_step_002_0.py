import cadquery as cq

# Parametric dimensions estimated from the image
block_width = 15.0      # Width of the rectangular base
block_height = 8.0      # Height of the rectangular base
block_length = 20.0     # Length of the straight section

transition_length = 25.0 # Length of the tapered section
tip_width = 30.0        # Width of the final flared tip
tip_height = 1.5        # Thickness of the final tip

# Create the model
# Step 1: Create the straight rectangular section
# We align the long axis along the X-axis
result = (
    cq.Workplane("YZ")
    .rect(block_width, block_height)
    .extrude(block_length)
)

# Step 2: Create the lofted transition
# We select the end face of the block, draw the matching rectangle,
# then offset a workplane to draw the wider, thinner tip profile.
result = (
    result.faces(">X")
    .workplane()
    .rect(block_width, block_height)        # Start profile of loft (matches block)
    .workplane(offset=transition_length)
    .rect(tip_width, tip_height)            # End profile of loft (flared tip)
    .loft(combine=True)                     # Create solid and union with base
)