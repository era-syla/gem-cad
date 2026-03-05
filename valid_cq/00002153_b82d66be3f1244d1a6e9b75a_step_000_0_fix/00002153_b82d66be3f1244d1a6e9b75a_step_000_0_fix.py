import cadquery as cq

# Parameters
outer_d = 80.0
wall_thickness = 3.0
height = 25.0
base_thickness = 3.0

shelf_width = 5.0   # radial width of the inner shelf ring
shelf_height = 4.0  # height of the inner shelf ring

post_count = 4
post_diameter = 5.0
post_hole_diameter = 2.0
post_radius = 25.0  # distance from center to post axis

slot_width = 10.0
slot_height = 10.0

# Derived
inner_radius = outer_d/2 - wall_thickness

# 1. Create the outer solid cylinder
outer = cq.Workplane("XY").circle(outer_d/2).extrude(height)

# 2. Hollow it leaving a base of thickness base_thickness
inner_cut = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(height - base_thickness)
    .translate((0, 0, base_thickness))
)
body = outer.cut(inner_cut)

# 3. Add the inner shelf ring on the bottom
shelf_outer_r = inner_radius
shelf_inner_r = inner_radius - shelf_width
shelf_ring = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(shelf_outer_r)
    .circle(shelf_inner_r)
    .extrude(shelf_height)
)
body = body.union(shelf_ring)

# 4. Add standoff posts
post_height = height - base_thickness
posts = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .polarArray(post_radius, 0, 360, post_count)
    .circle(post_diameter/2)
    .extrude(post_height)
)
body = body.union(posts)

# 5. Drill holes through the posts
body = (
    body.faces(">Z")
    .workplane()
    .polarArray(post_radius, 0, 360, post_count)
    .hole(post_hole_diameter, post_height + 0.1)
)

# 6. Cut two slots through the side wall
slot_depth = wall_thickness + 1.0
# First slot at 0°
slot_cut1 = (
    cq.Workplane("XY")
    .box(slot_width, slot_depth, slot_height)
    .translate((outer_d/2 - wall_thickness/2, 0, height - slot_height/2))
)
# Second slot at 90°
slot_cut2 = slot_cut1.rotate((0,0,0), (0,0,1), 90)
body = body.cut(slot_cut1).cut(slot_cut2)

result = body
