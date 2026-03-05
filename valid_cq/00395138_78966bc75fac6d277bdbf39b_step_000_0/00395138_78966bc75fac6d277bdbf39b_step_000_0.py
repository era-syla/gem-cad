import cadquery as cq

# Parameters defining the geometry
radius = 12.0          # Radius of the main arcs
thickness = 4.0        # Thickness of the S-strip
height = 10.0          # Extrusion height (Z-axis)
block_len = 4.5        # Length of the end blocks
block_width = 6.0      # Width of the end blocks (thicker than strip)
overlap = 0.1          # Small overlap to ensure valid boolean union

# 1. Define the S-shaped path using two tangent semicircles
# Left arc: starts at (-2R, 0), goes to (0,0) via top
# Right arc: starts at (0,0), goes to (2R, 0) via bottom
path = (
    cq.Workplane("XY")
    .moveTo(-2 * radius, 0)
    .threePointArc((-radius, radius), (0, 0))
    .threePointArc((radius, -radius), (2 * radius, 0))
)

# 2. Create the main strip solid
# Offset the wire to create 2D profile, then extrude
strip = (
    path
    .offset2D(thickness / 2)
    .extrude(height)
)

# 3. Create the Left End Block
# Attached at (-2R, 0), extending downwards.
# Inner face aligns with the strip's inner surface.
# The block protrudes outwards (to the left/negative X).
left_inner_x = -2 * radius + thickness / 2
left_outer_x = left_inner_x - block_width
left_center_x = (left_inner_x + left_outer_x) / 2
# Center Y shifted to create overlap at y=0
left_center_y = (-block_len + overlap) / 2 

left_block = (
    cq.Workplane("XY")
    .moveTo(left_center_x, left_center_y)
    .rect(block_width, block_len + overlap)
    .extrude(height)
)

# 4. Create the Right End Block
# Attached at (2R, 0), extending upwards.
# Inner face aligns with the strip's inner surface.
# The block protrudes outwards (to the right/positive X).
right_inner_x = 2 * radius - thickness / 2
right_outer_x = right_inner_x + block_width
right_center_x = (right_inner_x + right_outer_x) / 2
# Center Y shifted to create overlap at y=0
right_center_y = (block_len - overlap) / 2

right_block = (
    cq.Workplane("XY")
    .moveTo(right_center_x, right_center_y)
    .rect(block_width, block_len + overlap)
    .extrude(height)
)

# 5. Combine the parts into the final result
result = strip.union(left_block).union(right_block)