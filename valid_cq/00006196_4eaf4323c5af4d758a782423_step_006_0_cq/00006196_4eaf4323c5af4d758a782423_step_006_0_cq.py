import cadquery as cq

# --- Parametric Dimensions ---
# The total width and length of the square base
tile_size = 100.0  

# The height of the base block before the faceted features
base_height = 10.0

# The height of the pyramid peaks relative to the top of the base
peak_height = 20.0

# --- Geometry Construction ---

# 1. Create the base block
# We start with a simple box centered on X and Y
base = cq.Workplane("XY").box(tile_size, tile_size, base_height)

# 2. Define the pyramid shape for one quadrant
# We will create a single pyramid and then mirror/pattern it.
# The pyramid base is a square of size (tile_size / 2).
# We can create a solid pyramid by lofting from a square base to a point.

# Calculate quadrant size
quad_size = tile_size / 2.0

# Create a single pyramid located in the first quadrant (+X, +Y)
# The center of the first quadrant relative to the origin is (quad_size/2, quad_size/2)
# We create a sketch on the top face of the base for the pyramid's base.
pyramid = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2)  # Move to top of base
    .center(quad_size / 2, quad_size / 2) # Center in the first quadrant
    .rect(quad_size, quad_size)       # Draw base rectangle
    .workplane(offset=peak_height)    # Move up for the peak
    .circle(0.001)                    # Draw a tiny circle (effectively a point) for the apex
    .loft(combine=False)              # Create the pyramid solid
)

# 3. Create the pattern by mirroring the single pyramid
# We need 4 pyramids total. We can mirror the first one across X and Y planes.

# Mirror across YZ plane (X axis mirror)
pyramid_x_mirror = pyramid.mirror("YZ")

# Mirror both original and X-mirrored across XZ plane (Y axis mirror)
pyramid_y_mirror = pyramid.mirror("XZ")
pyramid_xy_mirror = pyramid_x_mirror.mirror("XZ")

# 4. Combine everything
# Union the base with all the pyramids
result = base.union(pyramid).union(pyramid_x_mirror).union(pyramid_y_mirror).union(pyramid_xy_mirror)

# Alternatively, a more procedural approach without mirrors for cleaner code logic:
# We could iterate and place them, but mirroring ensures symmetry perfectly.
# The logic above creates the "X" cross pattern of valleys seen in the image.
# Let's double check the image.
# The image shows a central low point where the 4 squares meet? No, looking closer:
# The center of the entire tile is a vertex where 4 edges meet.
# The corners of the tile are low.
# The midpoints of the outer edges are low.
# The center of each quadrant is a HIGH point (a peak).
# Let's re-examine the image.
# It looks like 4 pyramids.
# The center of the tile is a valley (intersection of pyramid bases).
# The corners of the tile are valleys.
# The peaks are in the center of each of the 4 sub-squares.
# This matches the construction logic above: 4 pyramids placed on a base.

# Final Result
if "show_object" in locals():
    show_object(result)