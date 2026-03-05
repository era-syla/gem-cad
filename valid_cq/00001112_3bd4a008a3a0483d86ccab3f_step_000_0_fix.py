import cadquery as cq

# Mug parameters
outer_radius = 35
inner_radius = 31
height = 80
wall = 4
bottom_thickness = 4

# Handle parameters
handle_width = 12
handle_depth = 8
handle_height = 50
handle_offset_x = outer_radius
handle_gap = 10  # inner opening

# Create the main cup body (cylinder)
cup = (
    cq.Workplane("XY")
    .cylinder(height, outer_radius)
)

# Hollow out the cup (keep bottom)
cup = (
    cup
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-(height - bottom_thickness))
)

# Create the handle as a rectangular frame
# Handle outer box
handle_outer_w = handle_depth + 8
handle_outer_h = handle_height + 8

handle_x = outer_radius + handle_depth / 2 + 2

# Build handle as a solid rectangular loop
# Outer rectangle of handle
handle_outer = (
    cq.Workplane("XZ")
    .center(outer_radius + handle_depth / 2 + 2, height / 2 - handle_height / 2 + handle_height / 2)
    .rect(handle_depth + 6, handle_height + 6)
    .extrude(handle_width)
)

# Inner cutout of handle
handle_inner = (
    cq.Workplane("XZ")
    .center(outer_radius + handle_depth / 2 + 2, height / 2 - handle_height / 2 + handle_height / 2)
    .rect(handle_depth - 2, handle_height - 8)
    .extrude(handle_width)
)

# Subtract inner from outer to make handle loop
handle = handle_outer.cut(handle_inner)

# Shift handle to be centered in Y
handle = (
    cq.Workplane("XZ")
    .center(outer_radius + 5, 0)
    .rect(handle_depth + 4, handle_height)
    .extrude(handle_width)
    .translate((-handle_width / 2, 0, 0))
)

# Redo handle properly
# The handle is a U-shape or rectangular ring attached to the side of the cup
# Let's build it as: outer box minus inner box

hw = 8    # handle wall thickness (depth in X)
ht = handle_height  # handle total height
hd = handle_width   # handle thickness in Y direction

# Center of handle in X: outer_radius + hw/2
cx = outer_radius + hw / 2 + 2

handle_solid = (
    cq.Workplane("YZ")
    .center(0, height / 2 - 5)
    .rect(hd + 4, ht + 4)
    .extrude(hw + 4)
    .translate((outer_radius - 2, 0, 0))
)

handle_void = (
    cq.Workplane("YZ")
    .center(0, height / 2 - 5)
    .rect(hd - 4, ht - 10)
    .extrude(hw + 4)
    .translate((outer_radius - 2, 0, 0))
)

handle = handle_solid.cut(handle_void)

# Combine cup and handle
result = cup.union(handle)

# Select edges on handle for small chamfer - skip chamfer to avoid errors
# Just output the result as is