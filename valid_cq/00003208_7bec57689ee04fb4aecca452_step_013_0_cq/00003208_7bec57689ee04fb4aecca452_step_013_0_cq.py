import cadquery as cq

# --- Parametric Dimensions ---
# Overall plate dimensions
length = 120.0  # Estimated length
width = 30.0    # Estimated width (height in the image orientation)
thickness = 6.0 # Estimated thickness

# Corner fillet radius
corner_radius = 5.0

# Hole dimensions
large_hole_diameter = 4.0
small_hole_diameter = 3.0

# Hole positions
# Assuming the origin is at the center of the plate
# Large holes (Left and Right)
large_hole_offset = (length / 2) - 10.0  # Distance from center to outer holes

# Small hole cluster pattern
# It looks like a V-shape or staggered pattern.
# Let's estimate coordinates relative to center (0,0)
# Top row of small holes
top_row_y = 5.0
# Bottom row of small holes
bottom_row_y = -5.0

# X-coordinates for small holes
# There seem to be 5 small holes.
# - One center-left top
# - One center-right top
# - One far-left bottom
# - One center bottom
# - One far-right bottom (wait, looking closer at the cluster)

# Let's re-examine the cluster.
# Left side: large hole
# Middle cluster:
#   - Top row: 2 holes
#   - Bottom row: 3 holes
# Right side: large hole

# Let's define the offsets for the small cluster
# Top row x-offsets
small_top_x1 = -15.0
small_top_x2 = 15.0

# Bottom row x-offsets
small_bot_x1 = -15.0
small_bot_x2 = 0.0
small_bot_x3 = 15.0

# Re-evaluating the image carefully.
# It looks like there are two distinct patterns or maybe a standard mounting plate.
# Let's look at the holes from left to right:
# 1. Large hole (far left)
# 2. Small hole (top)
# 3. Small hole (bottom) - aligned vertically with #2? No, slightly offset.
# Let's try to match the visual pattern more generically.
# Pattern:
#  - Large hole left: x = -50 (approx)
#  - Cluster Left Top: x = -20, y = 5
#  - Cluster Left Bottom: x = -20, y = -5
#  - Cluster Middle Bottom: x = 0, y = -5
#  - Cluster Right Top: x = 10, y = 5 (Wait, looking at the image again)

# Let's simplify the observation.
# Left End: Large Hole
# Right End: Large Hole
# Middle Area:
#   Top row: 2 holes
#   Bottom row: 3 holes
# Let's assume a grid pitch. Maybe 10mm or 15mm.

# Revised Hole List based on visual spacing:
holes_large_coords = [
    (-length/2 + 10, 0),  # Far Left
    (length/2 - 10, 0)    # Far Right
]

# Small holes coords
# Visually estimating relative to center
# Top row: two holes
holes_small_coords = [
    (-15, 6),   # Top left of cluster
    (15, 6),    # Top right of cluster
    (-15, -6),  # Bottom left of cluster
    (0, -6),    # Bottom center of cluster
    (15, -6)    # Bottom right of cluster
]

# Correction: Looking really closely at the crop.
# There is a hole at top-left of the cluster.
# There is a hole at top-right of the cluster.
# There is a hole at bottom-left of the cluster.
# There is a hole at bottom-middle of the cluster.
# There is a hole at bottom-right of the cluster?
# Actually, the one on the right looks like it's just a single top hole.
# Let's look at the specific pattern:
# Far Left (Large)
# Then a pair (Top/Bottom) slightly to the left of center?
# Then a single Bottom one in center?
# Then a pair (Top/Bottom) to the right?
# No, the right side of the cluster only has a top hole?
# Let's assume symmetry for the cluster first, then adjust.
# The cluster looks like 5 holes forming a 'W' or 'M' shape.
# Top row: x=-15, x=15
# Bottom row: x=-15, x=0, x=15
# This creates a rectangular group of 6 minus one top-middle hole.
# This seems like a plausible standard bracket hole pattern.

# --- CadQuery Construction ---

# 1. Create the base plate
base = cq.Workplane("XY").box(length, width, thickness)

# 2. Round the corners (vertical edges)
# Select edges parallel to Z axis
result = base.edges("|Z").fillet(corner_radius)

# 3. Cut the large holes
# Select the top face
result = result.faces(">Z").workplane()
result = result.pushPoints(holes_large_coords).hole(large_hole_diameter)

# 4. Cut the small holes
# We need to define the specific list of points for the small holes
# Based on the "W" / 5-hole pattern hypothesis
# Let's fine tune the positions to look like the image.
# The image shows:
#  - Left large hole
#  - Gap
#  - Small hole (Top)
#  - Small hole (Bottom) -- these two look vertically aligned or close to it
#  - Small hole (Bottom) -- in the middle
#  - Small hole (Top)
#  - Small hole (Bottom) -- these two on the right of center look aligned
#  - Gap
#  - Right large hole

# Let's refine the small hole coordinates
small_hole_locations = [
    (-20, 5),   # Top Left
    (-20, -5),  # Bottom Left
    (0, -5),    # Bottom Middle
    (20, 5),    # Top Right
    (20, -5),   # Bottom Right
]

# Applying small holes
result = result.pushPoints(small_hole_locations).hole(small_hole_diameter)

# If we look extremely closely at the crop, the top-right small hole seems slightly further left than the bottom-right small hole.
# But for a parametric CAD model, symmetry is the best starting assumption unless specific asymmetry is obvious.
# The previous "W" shape (points at -20, 0, 20) seems robust.

# Final check of the generated variable name
# The prompt asks for 'result'

# Export/Show happens implicitly in many CQ environments, but the variable is key.