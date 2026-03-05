import cadquery as cq

# Parameters
length = 100.0   # Height of the plate
width = 60.0     # Width of the plate
thickness = 5.0  # Thickness of the plate

# Hole Parameters
# Small corner holes
corner_hole_diameter = 4.0
corner_hole_inset_x = 5.0  # Distance from edge to hole center
corner_hole_inset_y = 5.0  # Distance from top/bottom to hole center

# Middle side holes (counterbored/countersunk on edges)
side_hole_y = 0.0 # Centered vertically
# Judging by the image, these are cutouts on the edge, likely cylindrical cuts
side_cutout_diameter = 10.0
side_cutout_depth = 5.0 # How deep they go into the plate from the edge

# Central hole
center_hole_diameter = 5.0

# Large vertical holes (above and below center)
large_hole_diameter = 10.0
large_hole_offset_y = 20.0 # Distance from center

# Create the base plate
result = cq.Workplane("XY").box(width, length, thickness)

# Create the 4 corner holes
# Calculate positions based on insets
corner_positions = [
    (width/2 - corner_hole_inset_x, length/2 - corner_hole_inset_y),
    (-width/2 + corner_hole_inset_x, length/2 - corner_hole_inset_y),
    (width/2 - corner_hole_inset_x, -length/2 + corner_hole_inset_y),
    (-width/2 + corner_hole_inset_x, -length/2 + corner_hole_inset_y)
]

result = result.faces(">Z").workplane().pushPoints(corner_positions).hole(corner_hole_diameter)

# Create the central small hole
result = result.faces(">Z").workplane().hole(center_hole_diameter)

# Create the two larger vertical holes
vertical_hole_positions = [
    (0, large_hole_offset_y),
    (0, -large_hole_offset_y)
]
result = result.faces(">Z").workplane().pushPoints(vertical_hole_positions).hole(large_hole_diameter)

# Create the side cutouts
# These appear to be circular cutouts centered on the left and right edges.
# The image shows two large circular recesses on the side edges, 
# and potentially a small one on the right edge as well, but let's stick to the prominent features.
# Looking closely at the image:
# - There is a semi-circular cutout on the left edge.
# - There is a small circular hole near the right edge, middle height.
# Let's refine the interpretation:
# The image actually shows:
# 1. Four corner holes.
# 2. A central small hole.
# 3. Two large holes aligned vertically in the middle.
# 4. On the LEFT edge: A semi-circular cutout (looks like a hole centered on the edge).
# 5. On the RIGHT edge: A small hole, aligned with the vertical center but inset.

# Let's adjust the "side" features:

# Left Edge Cutout (Semi-circle)
left_cutout_pos = (-width/2, 0)
result = result.faces(">Z").workplane().pushPoints([left_cutout_pos]).hole(side_cutout_diameter)

# Right Edge Middle Hole
# It looks smaller than the large vertical holes, maybe same as corner holes?
# Let's assume it's the same as corner holes for consistency, or slightly larger.
right_mid_hole_inset = 5.0
right_mid_hole_pos = (width/2 - right_mid_hole_inset, 0)
result = result.faces(">Z").workplane().pushPoints([right_mid_hole_pos]).hole(corner_hole_diameter)

# Final result is stored in 'result' variable