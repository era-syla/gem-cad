import cadquery as cq

# Parameters
th = 20            # general thickness
gap = 200          # gap between posts
post_h = 400       # height of vertical posts
over = th          # overhang of top beam
foot_len = 80      # length of each foot
foot_ht = th       # height of foot profile
foot_cut = 20      # inset for foot angled ends
foot_depth = th    # depth of foot (front/back)

# Compute positions
post_spacing = gap + th
post_x = post_spacing/2

# Vertical post
post = cq.Workplane("XY").rect(th, th).extrude(post_h)

# Left post with slot
left_post = post.translate((-post_x, 0, 0))
left_post = (
    left_post
    .faces("<X")
    .workplane(origin=(0, 0, post_h/2))
    .rect(10, 30)
    .cutBlind(5)
)

# Right post
right_post = post.translate((post_x, 0, 0))

# Top beam
top_beam = (
    cq.Workplane("XY")
    .workplane(offset=post_h - th)
    .rect(gap + 2 * over, th)
    .extrude(th)
)

# Middle beam
mid_beam = (
    cq.Workplane("XY")
    .workplane(offset=post_h / 2)
    .rect(gap, th)
    .extrude(th)
)

# Foot profile points in XZ plane
fp = [
    (-foot_len/2 + foot_cut, 0),
    (-foot_len/2,        foot_ht/2),
    (-foot_len/2 + foot_cut, foot_ht),
    (foot_len/2 - foot_cut,  foot_ht),
    (foot_len/2,         foot_ht/2),
    (foot_len/2 - foot_cut, 0),
]

# Single foot
foot = cq.Workplane("XZ").polyline(fp).close().extrude(foot_depth)

# Left and right feet
left_foot = foot.translate((-post_x, 0, 0))
right_foot = foot.translate((post_x, 0, 0))

# Assemble all parts
result = (
    left_post
    .union(right_post)
    .union(top_beam)
    .union(mid_beam)
    .union(left_foot)
    .union(right_foot)
)