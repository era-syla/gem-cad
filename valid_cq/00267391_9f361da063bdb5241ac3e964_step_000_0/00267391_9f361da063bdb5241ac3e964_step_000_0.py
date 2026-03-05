import cadquery as cq

# Dimensions
plate_width = 90.0
plate_height = 40.0
thickness = 3.0
fillet_radius = 6.0

# Feature Parameters
large_hole_diam = 12.0
small_hole_diam = 3.5
mount_hole_diam = 4.5
square_size = 5.0

# Feature Positions (relative to center (0,0))
large_hole_pos = (-22, 5)
rect_pos = (12, 6)
rect_dim = (14, 9)
slot_pos = (12, -1.5)
slot_dim = (14, 2)
square_pos = (35, 10)
small_holes_y = -7.0
small_holes_x = [-14, -4, 6]
mount_holes_pos = [(-30, -13), (22, -13)]

# 1. Base Plate
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 2. Circular Holes (Large hole, 3 small inline holes, 2 mounting holes)
# We collect all circular cut operations
result = (
    result.faces(">Z").workplane()
    # Large Hole
    .pushPoints([large_hole_pos])
    .hole(large_hole_diam)
    # Row of 3 small holes
    .pushPoints([(x, small_holes_y) for x in small_holes_x])
    .hole(small_hole_diam)
    # Mounting holes
    .pushPoints(mount_holes_pos)
    .hole(mount_hole_diam)
)

# 3. Rectangular Cuts (Main window, slot below it, square hole in corner)
result = (
    result.faces(">Z").workplane()
    # Rectangular Window
    .pushPoints([rect_pos])
    .rect(rect_dim[0], rect_dim[1])
    # Slot below window
    .pushPoints([slot_pos])
    .rect(slot_dim[0], slot_dim[1])
    # Square hole
    .pushPoints([square_pos])
    .rect(square_size, square_size)
    # Cut all rectangular profiles
    .cutThruAll()
)