import cadquery as cq

# Parameters
outer = 100
thick = 5
wall_h = 10
post_w = 10
post_h = 30
r = 20

# Outer frame walls
frame = (
    cq.Workplane("XY")
    .rect(outer, outer)
    .rect(outer - 2*thick, outer - 2*thick)
    .extrude(wall_h)
)

# Small rectangular block on front interior wall
small_block = (
    cq.Workplane("XY")
    .box(10, thick, wall_h)
    .translate((
        -25,                               # x position
        -outer/2 + thick/2,               # y position just inside front wall
        wall_h/2                          # z position
    ))
)

# Right-side interior partition
right_part = (
    cq.Workplane("XY")
    .box(thick, 20, wall_h)
    .translate((
        outer/2 - thick/2,                # x position just inside right wall
        -40,                              # y position
        wall_h/2
    ))
)

# Tall column in front-right interior corner
column = (
    cq.Workplane("XY")
    .box(post_w, post_w, post_h)
    .translate((
        outer/2 - thick - post_w/2,       # x flush with interior corner
        -outer/2 + thick + post_w/2,      # y flush with interior corner
        post_h/2
    ))
)

# Half-cylinder partition on front wall
# Full cylinder
cyl_full = (
    cq.Workplane("XY")
    .center(0, -outer/2 + thick + r)  # center placed r units inside front interior
    .circle(r)
    .extrude(wall_h)
)
# Box to cut the back half of the cylinder, keeping the front half
cut_box = (
    cq.Workplane("XY")
    .center(0, -outer/2 + thick + r)
    .rect(2*r, r)
    .extrude(wall_h)
)
semi_cyl = cyl_full.intersect(cut_box)

# Combine all parts
result = frame.union(small_block).union(right_part).union(column).union(semi_cyl)