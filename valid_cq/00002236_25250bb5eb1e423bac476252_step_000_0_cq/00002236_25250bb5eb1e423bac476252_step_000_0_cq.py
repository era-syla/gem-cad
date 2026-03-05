import cadquery as cq
import math

# --- Parameters ---
outer_radius = 50.0
inner_radius = 25.0
height = 30.0
num_segments = 3
gap_width = 2.0  # Width of the cut

# --- Geometry Construction ---

# 1. Create the base ring
base_ring = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)

# 2. Define the cutter
# The cuts in the image are tangential, originating from the inner circle.
# We will create a box that represents the cut and pattern it.
# The cutter needs to be long enough to slice through the outer wall.
cutter_length = outer_radius * 2.5
cutter_width = gap_width

# We create a single cutter positioned to make a tangential cut.
# A tangential cut from the inner radius can be achieved by positioning a rectangle
# such that one of its long edges is tangent to the inner circle, or offset slightly.
# Looking at the image, the cut seems to align with a tangent of the inner circle.
# Let's offset the cutter so its edge aligns with the inner radius.

cutter = (
    cq.Workplane("XY")
    .center(0, inner_radius + cutter_width/2) # Move to inner radius edge (plus half width to center it)
    # Actually, let's rethink. If the cut is tangent, the edge of the gap touches the inner circle.
    # Let's position a box such that its side is tangent to the inner circle.
    .center(cutter_length/2, -(inner_radius + cutter_width/2)) # Reset to center, move right
    .box(cutter_length, cutter_width, height * 2)
)

# However, the image shows the cuts are rotationally symmetric.
# A simpler way is to position the cutter relative to the origin and rotate it.
# The cut line appears to go from a point on the inner circle outwards.
# Let's define a cutter that is offset from the center by the inner radius.

# Improved cutter strategy:
# Create a rectangular box.
# Translate it along X so it starts near the origin.
# Translate it along Y by `inner_radius` so its bottom edge is tangent to the inner circle.
# But wait, looking at the image, the cut starts *into* the material.
# The "blade" of the cut seems to be tangent to the inner hole.

# Let's try creating a cutter that is offset in Y by `inner_radius` and extends along X.
# This would create a cut that grazes the inner hole.
# To account for the gap width, we might center the gap on that tangent line or offset it.
# The image shows a clean edge starting from the inner surface.
# Let's assume the cut is offset by `inner_radius`.

# Create a single cutter object
# We position a box such that it cuts a slot.
# Box dimensions: (large_length, gap_width, large_height)
# Position:
# X: We want it to start slightly behind X=0 to ensure a clean cut, extending outwards.
# Y: Offset by `inner_radius`.
cutter = (
    cq.Workplane("XY")
    .box(outer_radius * 3, gap_width, height * 2) # Create a long, thin, tall box
    .translate((outer_radius * 1.5, inner_radius, 0)) # Move it out along X and up by inner_radius
)

# 3. Create the pattern of cutters
# We need 3 cutters rotated by 120 degrees each.
cutters = cutter
for i in range(1, num_segments):
    angle = i * (360.0 / num_segments)
    rotated_cutter = cutter.rotate((0, 0, 0), (0, 0, 1), angle)
    cutters = cutters.union(rotated_cutter)

# 4. Subtract cutters from the base ring
result = base_ring.cut(cutters)

# Optional: Fillet edges if needed, but the image shows sharp edges.
# The current result should match the "iris" mechanism style ring segments.