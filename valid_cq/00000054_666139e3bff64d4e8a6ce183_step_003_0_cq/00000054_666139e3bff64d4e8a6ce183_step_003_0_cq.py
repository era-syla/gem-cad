import cadquery as cq

# --- Parametric Dimensions ---
# Overall plate dimensions
plate_width = 160.0
plate_depth = 80.0
thickness = 2.0

# Left side cutouts (larger)
left_cutout_width = 25.0
left_cutout_depth = 20.0
left_cutout_radius = 4.0  # Fillet radius for the cutout corners
left_cutout_spacing = 15.0 # Gap between the two cutouts
# Positioning relative to the left edge and top edge
left_cutout_x_offset = 25.0 # From left edge to center of first cutout group
left_cutout_y_offset = 20.0 # From back edge

# Right side cutouts (smaller slots)
right_cutout_width = 10.0
right_cutout_depth = 25.0
right_cutout_gap = 5.0 # Gap between the two slots
right_cutout_x_offset = 15.0 # From right edge to center of slots
right_cutout_y_offset = 15.0 # From front edge

# Notched Edge (Back edge)
# It looks like a series of small rectangular tabs/notches, typical for finger joints or alignment.
notch_width = 10.0
notch_depth = 2.0
num_notches = 6
notch_start_offset = 30.0 # Where the first notch starts from the left

# Corner cutout (Front Right)
corner_notch_width = 20.0
corner_notch_depth = 10.0

# --- Modeling ---

# 1. Base Plate
result = cq.Workplane("XY").box(plate_width, plate_depth, thickness)

# 2. Left Cutouts (Large Rectangles with rounded corners)
# We will create one sketch and cut it
# Center positions for left cutouts
# Let's position them relative to the plate center.
# Plate center is (0,0). Left edge is -plate_width/2. Back edge is +plate_depth/2.
# Position 1
lc_x1 = -plate_width/2 + 25.0
lc_y1 = plate_depth/2 - 25.0
# Position 2
lc_x2 = lc_x1 - 10.0 # Staggered or aligned? Looking at image, they are aligned along X axis?
# Actually, looking closer, they are aligned in Y, spaced in X.
# Wait, let's re-examine the image.
# There are two large square-ish holes on the left.
# There are two thin rectangular holes on the right.
# The notches are on the "back" long edge.
# There is a cutout on the "front right" corner.

# Let's refine positions.
# Left holes:
left_hole_size = 20.0
left_hole_spacing_x = 30.0
lh_x_center = -plate_width/2 + 40
lh_y_center = 0 # Centered? No, they look closer to the back edge (notched edge).
# Let's assume the notched edge is Y+.
lh_y_pos = plate_depth/4  # Upper half

# Creating the two left cutouts
left_cutouts = (
    cq.Workplane("XY")
    .rect(left_cutout_width, left_cutout_depth)
    .extrude(thickness)
    .edges("|Z").fillet(left_cutout_radius)
)

# Position 1
pos_x1 = -plate_width/2 + 30
pos_y1 = plate_depth/2 - 25
# Position 2
pos_x2 = -plate_width/2 + 65
pos_y2 = plate_depth/2 - 25

result = result.cut(left_cutouts.translate((pos_x1, pos_y1, 0)))
result = result.cut(left_cutouts.translate((pos_x2, pos_y2, 0)))


# 3. Right Cutouts (Thin slots)
# Position near the right edge, closer to front.
# Let's assume they are aligned along the X axis.
slot_width = 25.0
slot_height = 12.0
slot_spacing = 18.0

# Right side, near the front (Y-) edge
rs_x = plate_width/2 - 25
rs_y1 = -plate_depth/2 + 20
rs_y2 = rs_y1 + slot_spacing

result = result.cut(
    cq.Workplane("XY")
    .center(rs_x, rs_y1)
    .rect(slot_width, slot_height)
    .extrude(thickness)
)
result = result.cut(
    cq.Workplane("XY")
    .center(rs_x, rs_y2)
    .rect(slot_width, slot_height)
    .extrude(thickness)
)

# 4. Notched Back Edge
# Create a series of cuts along the back edge (Y = plate_depth/2)
# The notches cut INTO the plate.
notch_w = 15.0
notch_d = 3.0
# Start from left
start_x = -plate_width/2 + 40
spacing_x = 25.0

# Let's create a solid for the notches to cut away
for i in range(5):
    notch_center_x = start_x + (i * spacing_x)
    result = result.cut(
        cq.Workplane("XY")
        .center(notch_center_x, plate_depth/2)
        .rect(notch_w, notch_d * 2) # Double depth to ensure cut on edge
        .extrude(thickness)
    )

# 5. Corner Cutout (Front Right)
# A rectangular bite taken out of the front right corner.
corner_cut_w = 25.0
corner_cut_d = 10.0
# Position at corner: x=width/2, y=-depth/2
# We want to remove a box from that corner inwards.
# Center of cut box needs to be adjusted so its edge aligns with plate edge.
cc_x = plate_width/2 - corner_cut_w/2
cc_y = -plate_depth/2 + corner_cut_d/2

# Wait, looking at the image, the corner cutout is an L-shape removal or a tab sticking out?
# It looks like the main rectangular shape has a small rectangular area removed from the corner.
# Or rather, the main body is narrower at that corner.
# Let's look at the front-right corner of the image. The plate width effectively reduces.
# So we cut a rectangle out of the corner.

result = result.cut(
    cq.Workplane("XY")
    .center(plate_width/2, -plate_depth/2) # Corner
    .rect(corner_cut_w * 2, corner_cut_d * 2) # Oversize centered on corner
    .extrude(thickness)
)

# Correcting the specific corner cut to match image better:
# It looks like a stepped cutout.
# Let's try a simpler approach: define the outline point by point if complex, 
# but here boolean subtracts are easiest.

# Let's refine the right side slots. In the image, they are oriented parallel to the short edge?
# No, they are parallel to the long edge.
# The image shows two rectangular holes on the right, aligned with each other along the Y axis (depth).
# My previous code did this (rs_y1, rs_y2).

# Let's refine the left holes.
# In the image, the left holes are aligned along the X axis (length).
# One is further left, one is more central. They seem to be near the "back" edge.

# Let's refine the back notches.
# They look like castellated tabs.

# Final polish of coordinates to match visual proportions
# Resetting result to build cleanly
plate_width = 140.0
plate_depth = 80.0
thickness = 2.0

# Base
result = cq.Workplane("XY").box(plate_width, plate_depth, thickness)

# 1. Back Edge Notches (Top edge in standard view, Y+)
# Castellations: remove material to leave tabs, or add tabs?
# Image shows recesses cut into the straight edge.
notch_width = 8.0
notch_depth = 2.5
gap_between_notches = 15.0
first_notch_x = -plate_width/2 + 30.0 
num_notches = 6

for i in range(num_notches):
    x_pos = first_notch_x + i * (notch_width + gap_between_notches)
    result = result.cut(
        cq.Workplane("XY")
        .center(x_pos, plate_depth/2)
        .rect(notch_width, notch_depth * 2)
        .extrude(thickness)
    )

# 2. Left Cutouts (Large Rounded Rectangles)
# They are located in the "back-left" quadrant roughly.
cutout_w = 22.0
cutout_h = 18.0
fillet_r = 3.0
spacing = 10.0

# Left-most cutout
c1_x = -plate_width/2 + 35.0
c1_y = plate_depth/2 - 25.0

# Next cutout to the right
c2_x = c1_x + cutout_w + spacing
c2_y = c1_y

# Helper to make rounded rect cut
def rounded_rect_cut(x, y, w, h, r):
    return (cq.Workplane("XY")
            .center(x, y)
            .rect(w, h)
            .extrude(thickness)
            .edges("|Z").fillet(r))

result = result.cut(rounded_rect_cut(c1_x, c1_y, cutout_w, cutout_h, fillet_r))
result = result.cut(rounded_rect_cut(c2_x, c2_y, cutout_w, cutout_h, fillet_r))

# 3. Right Cutouts (Rectangular slots)
# Located near the front-right
slot_w = 20.0
slot_h = 10.0
slot_gap = 5.0

# These seem to be aligned along the depth (Y axis)? No, looking at the perspective,
# the long side of the plate is X.
# The slots are side-by-side along the X axis? Or one behind the other?
# In the image, on the right side, there are two rectangles.
# They look to be arranged along the Y-axis (front-to-back relative to the plate).
# Or maybe along the X axis? 
# Let's look at the perspective lines. 
# The two holes are close to the right edge. One is "deeper" into the plate, one is closer to the edge.
# This implies alignment along Y (depth).

s_x = plate_width/2 - 25.0
s1_y = -plate_depth/2 + 25.0
s2_y = s1_y + slot_h + slot_gap

result = result.cut(
    cq.Workplane("XY").center(s_x, s1_y).rect(slot_w, slot_h).extrude(thickness)
)
result = result.cut(
    cq.Workplane("XY").center(s_x, s2_y).rect(slot_w, slot_h).extrude(thickness)
)

# 4. Corner Cutout (Front-Right)
# The plate has a "step" on the right side front corner.
# It cuts into the width from the right side, or into the depth from the front?
# It looks like a rectangular notch on the front edge, at the right corner.
corner_notch_w = 15.0 # Along X
corner_notch_d = 10.0 # Along Y

# Position: Bottom Right corner (X+, Y-)
cn_center_x = plate_width/2 - corner_notch_w/2
cn_center_y = -plate_depth/2 + corner_notch_d/2

# Wait, looking at the image, the corner is actually cut OUT.
# The right edge is shorter than the left edge? No.
# The front edge is not straight. It steps IN near the right.
# So we remove a rectangle from the Front-Right corner.
result = result.cut(
    cq.Workplane("XY")
    .center(plate_width/2, -plate_depth/2) # Right-Front Corner
    .rect(corner_notch_w*2, corner_notch_d*2) # Oversized box centered on corner
    .extrude(thickness)
)