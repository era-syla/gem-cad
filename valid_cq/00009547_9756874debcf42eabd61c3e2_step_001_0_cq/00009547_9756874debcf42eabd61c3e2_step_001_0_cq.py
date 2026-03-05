import cadquery as cq

# --- Parametric Dimensions ---
length = 100.0   # Total length of the block
height = 80.0    # Total height of the block
width = 30.0     # Thickness of the block

# Dimensions for the rectangular hole
hole_length = 60.0
hole_height = 40.0

# --- Geometry Construction ---

# 1. Start with a solid block
# 2. Cut a rectangular through-hole centered on the face
result = (
    cq.Workplane("XY")
    .box(length, height, width)  # Create the main body
    .faces(">Z")                 # Select the top face (relative to creation plane) - actually, let's just cut through Z
    .workplane()
    .rect(hole_length, hole_height) # Sketch the rectangle for the hole
    .cutThruAll()                # Cut the rectangle through the entire block
)

# Alternatively, a more explicit face selection approach to match the visual orientation:
# The image shows the thickness along one axis, let's say Y or X, and the profile on the other.
# Let's align it so "XY" is the face with the hole, and "Z" is the thickness.

thickness = 30.0
outer_width = 100.0
outer_height = 80.0
inner_width = 60.0
inner_height = 40.0

result = (
    cq.Workplane("XY")
    .box(outer_width, outer_height, thickness)  # Create the base block
    .faces(">Z")                                # Select the front face
    .workplane() 
    .rect(inner_width, inner_height)            # Sketch the inner rectangle
    .cutThruAll()                               # Cut through the block
)