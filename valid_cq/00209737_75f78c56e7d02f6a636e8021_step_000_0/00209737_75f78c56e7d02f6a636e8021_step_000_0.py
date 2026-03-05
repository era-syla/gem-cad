import cadquery as cq

# Dimensions
width = 15      # Narrow dimension (visible on left)
depth = 30      # Wide dimension (visible on right)
height_left = 70
height_top = 45
height_right = 30

# Spacing/Offsets
gap_x = 20      # Horizontal spacing between centers
offset_y_top = 20   # Y-offset for the top box (pushed back)
offset_y_right = 10 # Y-offset for the right box
lift_top = 45   # Z-elevation for the top box base
lift_right = 25 # Z-elevation for the right box base

# Create the left box (tallest, at origin)
# Centered=False for Z puts the base at z=0
box_left = (
    cq.Workplane("XY")
    .box(width, depth, height_left, centered=(True, True, False))
)

# Create the top box (medium, lifted and shifted)
box_top = (
    cq.Workplane("XY")
    .workplane(offset=lift_top)
    .center(gap_x, offset_y_top)
    .box(width, depth, height_top, centered=(True, True, False))
)

# Create the right box (shortest, lifted slightly and shifted further right)
box_right = (
    cq.Workplane("XY")
    .workplane(offset=lift_right)
    .center(gap_x * 2, offset_y_right)
    .box(width, depth, height_right, centered=(True, True, False))
)

# Combine all boxes into a single object
result = box_left.union(box_top).union(box_right)