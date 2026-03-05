import cadquery as cq

# Parametric definitions
block_size = 50.0  # Size of the main cube (LxWxH)
large_hole_diameter = 40.0
small_hole_diameter = 30.0
large_hole_depth = 10.0
small_hole_depth = 25.0 # Total depth from top surface or specific depth of the second cut

# Create the base block
# We center the box to make origin-based operations easier
result = cq.Workplane("XY").box(block_size, block_size, block_size)

# Create the larger counterbore hole
# We select the top face, work on it, and cut a hole
result = result.faces(">Z").workplane().hole(large_hole_diameter, large_hole_depth)

# Create the smaller thru or deeper hole
# We select the bottom face of the previous cut (or just work from the top again)
# Working from the top again is often more robust parametrically
result = result.faces(">Z").workplane().hole(small_hole_diameter, large_hole_depth + small_hole_depth)

# Alternatively, to match the "stepped" look exactly if the second hole is blind:
# 1. Base Cube
# 2. Cut larger circle down by 'large_hole_depth'
# 3. Cut smaller circle down by total depth
# The .hole() method handles centering automatically on the selected workplane.