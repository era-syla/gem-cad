import cadquery as cq

# Parametric dimensions
height = 100.0      # Total height of the extrusion
width = 60.0        # Total width of the U-shape
depth = 40.0        # Depth of the U-shape (flange length)
thickness = 10.0    # Wall thickness

# Create the U-channel profile
# We start with a base rectangle representing the outer boundary
# and subtract an inner rectangle to create the "U" shape, then extrude.

# Create the main body block
outer_block = cq.Workplane("XY").box(width, depth, height)

# Create the cutout block to form the channel
# The cutout width is (width - 2 * thickness)
# The cutout depth is (depth - thickness)
# The cutout needs to be positioned correctly to leave the back wall and side walls.
# We align the cutout to the "front" face (relative to depth) so it cuts through.

cutout_width = width - (2 * thickness)
cutout_depth = depth - thickness

# We create the result by making the solid block and cutting away the center
result = (
    outer_block
    .faces(">Y")  # Select the front face (in Y direction)
    .workplane()
    .center(0, 0) # Center on the face
    # We want to cut a rectangle. The outer block is centered at origin.
    # We shift the cut downwards (in local Y, which is global Z)? No, the workplane handles orientation.
    # Let's think in 2D profile extrusion instead, it's often cleaner.
)

# Alternative cleaner approach: Sketch the U-shape and extrude
result = (
    cq.Workplane("XY")
    .rect(width, depth)            # Base outer rectangle
    .extrude(height)               # Extrude to create solid block
    .faces(">Y")                   # Select the "front" face
    .workplane()
    .rect(width - 2*thickness, height) # Create rectangle for the cutout (full height)
    .cutBlind(-(depth - thickness))   # Cut inwards, leaving the back wall thickness
)
