import cadquery as cq

# Parameters
base_length = 50.0
base_width = 5.0
base_height = 8.0
base_chamfer = 2.0
base_cut_length = 30.0
base_cut_height = 2.0

vertical_post_width = 5.0
vertical_post_thickness = 5.0
vertical_post_height = 70.0

crossbar_length = 60.0
crossbar_width = 5.0
crossbar_thickness = 5.0

topbar_length = 70.0
topbar_width = 5.0
topbar_height = 8.0

assembly_width = 60.0

# Base feet
base_profile = (
    cq.Workplane("YZ")
    .rect(base_length, base_height)
    .extrude(base_width)
)

# Apply chamfers to the top corners of the base
base_foot = (
    base_profile
    .edges(">Z and >Y").chamfer(base_chamfer)
    .edges(">Z and <Y").chamfer(base_chamfer)
)

# Cut the bottom of the base
base_cut = (
    cq.Workplane("YZ")
    .workplane(offset=-base_width/2)
    .center(0, -base_height/2)
    .rect(base_cut_length, base_cut_height * 2)
    .extrude(base_width)
)

base_foot = base_foot.cut(base_cut)

# Vertical posts
vertical_post = (
    cq.Workplane("XY")
    .rect(vertical_post_thickness, vertical_post_width)
    .extrude(vertical_post_height)
)

# Crossbar
crossbar = (
    cq.Workplane("XY")
    .rect(crossbar_length, crossbar_width)
    .extrude(crossbar_thickness)
)

# Topbar
topbar = (
    cq.Workplane("XY")
    .rect(topbar_length, topbar_width)
    .extrude(topbar_height)
)

# Assembly
left_foot = base_foot.translate((assembly_width/2, 0, base_height/2))
right_foot = base_foot.translate((-assembly_width/2, 0, base_height/2))

left_post = vertical_post.translate((assembly_width/2, 0, base_height))
right_post = vertical_post.translate((-assembly_width/2, 0, base_height))

mid_crossbar = crossbar.translate((0, 0, base_height + vertical_post_height/3))

top_bar = topbar.translate((0, 0, base_height + vertical_post_height))

# Combine all parts
result = (
    cq.Workplane("XY")
    .union(left_foot)
    .union(right_foot)
    .union(left_post)
    .union(right_post)
    .union(mid_crossbar)
    .union(top_bar)
)

# Add tenon details (visual cuts on the outside of posts)
tenon_cut = (
    cq.Workplane("YZ")
    .rect(crossbar_width, crossbar_thickness)
    .extrude(vertical_post_thickness)
)

left_tenon = tenon_cut.translate((assembly_width/2 + vertical_post_thickness/2, 0, base_height + vertical_post_height/3 + crossbar_thickness/2))
right_tenon = tenon_cut.translate((-assembly_width/2 - vertical_post_thickness/2, 0, base_height + vertical_post_height/3 + crossbar_thickness/2))

# Result is already combined