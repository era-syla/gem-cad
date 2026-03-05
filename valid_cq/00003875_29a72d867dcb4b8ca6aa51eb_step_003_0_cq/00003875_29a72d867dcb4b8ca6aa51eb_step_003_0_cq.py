import cadquery as cq

# --- Parameters ---
# Dimensions estimated from visual inspection
length = 150.0  # Total length of the plate
width = 40.0    # Total width of the plate
thickness = 2.0 # Thickness of the material

# Notch details
notch_depth = 5.0
notch_width = 4.0

# Rectangular cutout details
rect_cut_width = 10.0
rect_cut_height = 8.0
rect_cut_x_pos = -50.0 # Relative to center

# Small hole/cutout details
small_notch_x_pos = 10.0
small_notch_size = 3.0

# End tab/notch details
end_notch_depth = 4.0
end_notch_width = 8.0

# --- Geometry Construction ---

# 1. Base Plate
# Create the base rectangular plate
base = cq.Workplane("XY").box(length, width, thickness)

# 2. Side Notches
# There appear to be notches on one long edge.
# Let's assume notches are on the "positive Y" face in the 2D sketch plane,
# but since box creates a centered object, we work relative to that.

# Notch 1: Near the left end
notch1 = (
    cq.Workplane("XY")
    .rect(notch_width, notch_depth * 2) # Make it deep enough to cut through edge
    .extrude(thickness)
    .translate((-length/2 + 20, width/2, 0)) # Position on edge
)

# Notch 2: Near the center
notch2 = (
    cq.Workplane("XY")
    .rect(notch_width, notch_depth * 2)
    .extrude(thickness)
    .translate((10, width/2, 0)) # Position on edge
)

# 3. End Notches / Features
# The ends have a stepped profile or a notch. 
# Left End Notch
left_end_notch = (
    cq.Workplane("XY")
    .rect(end_notch_depth * 2, end_notch_width)
    .extrude(thickness)
    .translate((-length/2, width/2 - 10, 0)) # Offset from corner
)

# Right End Notch
right_end_notch = (
    cq.Workplane("XY")
    .rect(end_notch_depth * 2, end_notch_width)
    .extrude(thickness)
    .translate((length/2, width/2 - 10, 0))
)

# 4. Internal Cutouts
# Rectangular hole
rect_hole = (
    cq.Workplane("XY")
    .rect(rect_cut_width, rect_cut_height)
    .extrude(thickness)
    .translate((-length/3, width/4, 0))
)

# Small slot/hole near the other end
# It looks like a small angled slot or just a small rectangle
slot_hole = (
    cq.Workplane("XY")
    .rect(8.0, 3.0)
    .extrude(thickness)
    .translate((length/3, width/4, 0))
    .rotate((0,0,0), (0,0,1), 45) # Slight rotation if it looks angled
)

# --- Combine Operations ---

# Start with base
part = base

# Subtract side notches
part = part.cut(notch1).cut(notch2)

# Subtract end features
part = part.cut(left_end_notch).cut(right_end_notch)

# Subtract internal holes
part = part.cut(rect_hole).cut(slot_hole)


# --- Pattern Creation ---
# The image shows two identical parts. We will create the second one 
# by translating the first one.

part2 = part.translate((0, -width * 2.5, 0))

# Combine both into the final result
result = part.union(part2)
