import cadquery as cq

# --- Parameters ---
# Main plate dimensions
plate_length = 100.0
plate_width = 50.0
plate_thickness = 10.0
corner_radius = 2.0  # Fillet on the vertical corners

# Center circular feature
center_pocket_diam = 30.0
center_pocket_depth = 3.0
center_hole_diam = 10.0

# Medium holes (off-center pair)
medium_hole_diam = 12.0
medium_hole_x_offset = 25.0
medium_hole_y_offset = 12.0 # Looks slightly off center-line, but let's assume mirrored or positioned
# Looking closely at the image, these two holes are on a diagonal.
# One is bottom-left quadrant, one is top-right quadrant.
# Let's estimate their coordinates relative to center.
med_hole_1_pos = (-20.0, -12.0)
med_hole_2_pos = (30.0, 5.0) 
# Actually, looking at the symmetry, the medium holes look mirrored across the center point.
# Let's assume symmetry for a better parametric model.
med_hole_dist_x = 40.0 # Distance from center
med_hole_dist_y = 10.0 # Distance from center
# Looking closer at image:
# There is a big center hole.
# There is a medium hole to the "left-bottom" of the center.
# There is a medium hole to the "right-top" (slightly different y?) of the center.
# Actually, let's assume a simpler symmetric layout often found in mounting plates.
# Let's place them diagonally.
med_hole_offset_x = 25.0
med_hole_offset_y = 10.0


# Small mounting holes (corners and sides)
small_hole_diam = 4.0
small_cbore_diam = 7.0 # Counterbore diameter (visible on the top face)
small_cbore_depth = 2.0

# Coordinates for small holes
# Looks like 4 corners + 2 near the middle
# Let's define offsets from center
outer_hole_dx = (plate_length / 2) - 5.0
outer_hole_dy = (plate_width / 2) - 5.0

mid_small_hole_dx = 15.0 # Closer to center
mid_small_hole_dy = (plate_width / 2) - 10.0


# --- Modeling ---

# 1. Base Plate
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Center Feature (Pocket + Through Hole)
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(center_hole_diam) # Through hole
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(center_pocket_diam / 2)
    .cutBlind(-center_pocket_depth) # Pocket
)

# 3. Medium Offset Holes (Through holes)
# Looking at the image, the one on the left is below the centerline, 
# the one on the right is above the centerline.
# Left Hole
result = (
    result
    .faces(">Z")
    .workplane()
    .center(-20.0, -12.0)
    .hole(medium_hole_diam)
)
# Right Hole
result = (
    result
    .faces(">Z")
    .workplane() # Reset origin
    .center(30.0, 5.0)
    .hole(medium_hole_diam)
)


# 4. Small Counterbored Mounting Holes
# Four corners
corner_pts = [
    (-outer_hole_dx, -outer_hole_dy),
    (outer_hole_dx, -outer_hole_dy),
    (outer_hole_dx, outer_hole_dy),
    (-outer_hole_dx, outer_hole_dy)
]

# Two inner small holes
# Looking at image:
# One is near the left, above the centerline (opposite the medium hole)
# One is near the right, below the centerline (opposite the medium hole)
inner_small_pts = [
    (-25.0, 10.0),
    (25.0, -10.0)
]

all_small_hole_pts = corner_pts + inner_small_pts

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(all_small_hole_pts)
    .cboreHole(small_hole_diam, small_cbore_diam, small_cbore_depth)
)