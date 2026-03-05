import cadquery as cq

# Main box dimensions
box_l = 80
box_w = 50
box_h = 35
wall = 4
floor_h = 5

# Create the outer box
outer = (
    cq.Workplane("XY")
    .box(box_l, box_w, box_h, centered=(True, True, False))
)

# Shell it (remove top face)
outer = outer.faces(">Z").shell(-wall)

# Now create the inner cavity features
# The divider/saddle shape in the middle - a raised platform with a curved saddle

# Create the base result from the shelled box
result = (
    cq.Workplane("XY")
    .box(box_l, box_w, box_h, centered=(True, True, False))
    .faces(">Z")
    .shell(-wall)
)

# Add a central raised mound/saddle feature inside
# Create a cylinder-like mound in the center
mound = (
    cq.Workplane("XY")
    .workplane(offset=floor_h)
    .cylinder(box_h - floor_h - wall, 12, centered=(True, True, False))
)

# Create the saddle divider - a box that spans the width
divider = (
    cq.Workplane("XY")
    .workplane(offset=floor_h)
    .box(wall * 1.5, box_w - wall * 2 - 2, box_h - floor_h - wall,
         centered=(True, True, False))
    .translate((0, 0, 0))
)

# Build inner raised platform with saddle shape using a profile
# Saddle: raised in center with curved notches on front/back

# Create the saddle shape by making a box and cutting curved notches
saddle_h = box_h - wall - 2
saddle_w = 20
saddle_l = box_w - wall * 2 - 4

# Center saddle block
saddle_block = (
    cq.Workplane("XY")
    .box(saddle_w, saddle_l, saddle_h, centered=(True, True, False))
    .translate((0, 0, floor_h))
)

# Cut curved notch from front of saddle
notch_r = 10
notch_cyl_front = (
    cq.Workplane("XZ")
    .workplane(offset=-(saddle_l / 2 + 1))
    .circle(notch_r)
    .extrude(saddle_l + 2)
    .translate((0, -(saddle_l/2 + 1), floor_h + saddle_h * 0.6))
)

# Use a simpler approach: create the full model step by step
# Outer shell box
result = (
    cq.Workplane("XY")
    .box(box_l, box_w, box_h, centered=(True, True, False))
)

# Cut the inner cavity
inner_l = box_l - wall * 2
inner_w = box_w - wall * 2

result = (
    result
    .faces(">Z")
    .workplane()
    .rect(inner_l, inner_w)
    .cutBlind(-(box_h - floor_h))
)

# Add central raised post/mound
post_r = 11
post_h = box_h - floor_h - wall - 1

result = (
    result
    .workplane(offset=-(box_h - floor_h - post_h))
    .circle(post_r)
    .extrude(post_h)
)

# Cut saddle groove through the post from front to back
groove_r = 8
result = (
    result
    .workplane(offset=-(wall))  # top of box level
    .transformed(rotate=(90, 0, 0))
    .workplane(offset=0)
)

# Cut a curved channel across the top of the post
groove_cut = (
    cq.Workplane("XZ")
    .center(0, floor_h + post_h - groove_r + 3)
    .circle(groove_r)
    .extrude(box_w)
    .translate((0, -box_w/2, 0))
)

result = result.cut(groove_cut)

# Cut side notches on left and right
side_notch = (
    cq.Workplane("YZ")
    .center(0, floor_h + post_h - groove_r + 3)
    .circle(groove_r)
    .extrude(box_l)
    .translate((-box_l/2, 0, 0))
)

result = result.cut(side_notch)

# Apply fillets to soften edges
result = (
    result
    .edges("|Z")
    .fillet(3)
)