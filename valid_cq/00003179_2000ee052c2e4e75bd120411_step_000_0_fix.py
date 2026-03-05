import cadquery as cq

# Dimensions
outer_w = 80  # width (x)
outer_d = 60  # depth (y)
outer_h = 70  # height (z)
wall = 3       # wall thickness
floor_t = 3    # floor thickness

# Build the outer shell as a box
outer = (
    cq.Workplane("XY")
    .box(outer_w, outer_d, outer_h, centered=(True, True, False))
)

# Hollow out the inside - leave walls and floor
inner_cut = (
    cq.Workplane("XY")
    .box(outer_w - 2*wall, outer_d - 2*wall, outer_h - floor_t, centered=(True, True, False))
    .translate((0, 0, floor_t))
)

shell = outer.cut(inner_cut)

# Create the curved front cutout - arc cut from the front face
# The front is at y = -outer_d/2
# Cut a curved profile from the top-front
curve_cut = (
    cq.Workplane("XZ")
    .workplane(offset=-outer_d/2)
    .moveTo(-outer_w/2 + wall, outer_h)
    .lineTo(-outer_w/2 + wall, outer_h * 0.45)
    .threePointArc((0, outer_h * 0.35), (outer_w/2 - wall, outer_h * 0.45))
    .lineTo(outer_w/2 - wall, outer_h)
    .close()
    .extrude(wall + 1)
)

shell = shell.cut(curve_cut)

# Add back wall curved top - cut the back wall top with same curve but leave a lip
# Actually cut the open top of back panel with a curve
back_curve_cut = (
    cq.Workplane("XZ")
    .workplane(offset=outer_d/2 - wall - 0.01)
    .moveTo(-outer_w/2 + wall, outer_h)
    .lineTo(-outer_w/2 + wall, outer_h * 0.6)
    .threePointArc((0, outer_h * 0.5), (outer_w/2 - wall, outer_h * 0.6))
    .lineTo(outer_w/2 - wall, outer_h)
    .close()
    .extrude(wall + 0.1)
)

shell = shell.cut(back_curve_cut)

# Add internal dividers
# Vertical divider parallel to XZ plane (splits depth)
div1 = (
    cq.Workplane("XY")
    .workplane(offset=floor_t)
    .center(0, -outer_d/4 + 2)
    .rect(outer_w - 2*wall, wall)
    .extrude(outer_h * 0.7)
)

shell = shell.union(div1)

# Vertical dividers parallel to YZ plane (splits width)
div2 = (
    cq.Workplane("XY")
    .workplane(offset=floor_t)
    .center(-outer_w/4 + 2, 0)
    .rect(wall, outer_d - 2*wall)
    .extrude(outer_h * 0.8)
)

shell = shell.union(div2)

div3 = (
    cq.Workplane("XY")
    .workplane(offset=floor_t)
    .center(outer_w/4 - 2, 0)
    .rect(wall, outer_d - 2*wall)
    .extrude(outer_h * 0.8)
)

shell = shell.union(div3)

# Add mounting holes on the left side wall
left_wall_x = -outer_w/2

hole1 = (
    cq.Workplane("YZ")
    .workplane(offset=left_wall_x)
    .center(0, outer_h * 0.75)
    .circle(3)
    .extrude(wall + 1)
)

shell = shell.cut(hole1)

hole2 = (
    cq.Workplane("YZ")
    .workplane(offset=left_wall_x)
    .center(0, outer_h * 0.25)
    .circle(3)
    .extrude(wall + 1)
)

shell = shell.cut(hole2)

# Small screw holes on back wall
back_hole1 = (
    cq.Workplane("XZ")
    .workplane(offset=outer_d/2 - wall)
    .center(outer_w/4, outer_h * 0.6)
    .circle(2)
    .extrude(wall + 1)
)
shell = shell.cut(back_hole1)

back_hole2 = (
    cq.Workplane("XZ")
    .workplane(offset=outer_d/2 - wall)
    .center(-outer_w/4, outer_h * 0.6)
    .circle(2)
    .extrude(wall + 1)
)
shell = shell.cut(back_hole2)

result = shell