import cadquery as cq

# Main hollow square post
outer_size = 5
inner_size = 4
wall_thickness = 0.5
post_height = 60

# Create the hollow square tube (post)
post = (
    cq.Workplane("XY")
    .rect(outer_size, outer_size)
    .extrude(post_height)
    .faces(">Z")
    .workplane()
    .rect(inner_size, inner_size)
    .cutThruAll()
)

# Small C-channel/clip bracket next to the post
# Position it to the right and lower
clip_width = 4
clip_height = 3
clip_depth = 3
clip_wall = 0.5

# Create C-channel shape using a profile
# The C-channel is open on one side (like a U rotated 90 degrees)
clip_outer = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(9, 0, 2))
    .rect(clip_depth, clip_width)
    .extrude(clip_height)
)

# Cut the inner part to make C-shape (open on one side - front face)
clip_inner = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(9 + clip_wall, 0, 2))
    .rect(clip_depth, clip_width - 2 * clip_wall)
    .extrude(clip_height)
)

clip = clip_outer.cut(clip_inner)

# Cut the opening on the right side to make it a C-channel
clip_opening = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(9 + clip_depth / 2, 0, 2 + clip_wall))
    .rect(clip_depth, clip_width)
    .extrude(clip_height - clip_wall)
)

clip = clip.cut(clip_opening)

# Combine both parts
result = post.union(clip)