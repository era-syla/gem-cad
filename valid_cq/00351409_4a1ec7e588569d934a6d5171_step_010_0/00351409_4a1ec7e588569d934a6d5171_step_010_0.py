import cadquery as cq

# -- Parameters --
# Plate dimensions
plate_width = 100.0
plate_height = 220.0
plate_thickness = 10.0

# Hole parameters
hole_diameter = 6.5

# Coordinates calculation
# Right side holes: aligned vertically, near the right corners
right_hole_x = plate_width / 2 - 15.0  # 15mm from edge
right_hole_y = plate_height / 2 - 15.0 # 15mm from top/bottom

# Left side holes: arranged in two pairs
# Pattern observed: Outer hole is lower, Inner hole is higher (for both pairs)
left_outer_x = -plate_width / 2 + 15.0
left_inner_x = -plate_width / 2 + 30.0

# Vertical positioning for left pairs
pair_center_dist = 50.0 # Distance of the pair center from the plate horizontal centerline
pair_y_stagger = 10.0   # Vertical offset from the pair center for the holes

points = []

# 1. Top Right Hole
points.append((right_hole_x, right_hole_y))

# 2. Bottom Right Hole
points.append((right_hole_x, -right_hole_y))

# 3. Top Left Pair
# Inner hole is higher (+), Outer hole is lower (-) relative to pair center
points.append((left_outer_x, pair_center_dist - pair_y_stagger)) # Outer, Lower
points.append((left_inner_x, pair_center_dist + pair_y_stagger)) # Inner, Higher

# 4. Bottom Left Pair
# Pattern repeats: Inner hole is higher (less negative), Outer hole is lower (more negative)
points.append((left_outer_x, -pair_center_dist - pair_y_stagger)) # Outer, Lower
points.append((left_inner_x, -pair_center_dist + pair_y_stagger)) # Inner, Higher

# -- Modeling --
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(points)
    .hole(hole_diameter)
)