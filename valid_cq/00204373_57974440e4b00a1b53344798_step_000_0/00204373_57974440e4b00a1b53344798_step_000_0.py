import cadquery as cq

# Parametric dimensions based on visual estimation of the image
length = 200.0
width = 8.0        # The narrower dimension of the profile
height = 24.0      # The taller dimension of the profile
wall_thickness = 2.5

# Calculated dimensions for the slot
# The slot runs along the length, centered on the width
slot_width = width - (2 * wall_thickness)
# The slot goes deep but leaves a base connecting the two sides (U-channel profile)
slot_depth = height - wall_thickness

# Generate the geometry
# 1. Create a base rectangular prism centered at the origin
# 2. Select the top face (+Z)
# 3. Cut a rectangular slot along the entire length
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .faces("+Z")
    .workplane()
    # Create a rectangle for the cut. 
    # Length is slightly exaggerated (length + 5) to ensure it cuts cleanly through both ends.
    .rect(length + 5.0, slot_width)
    .cutBlind(-slot_depth)
)