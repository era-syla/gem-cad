import cadquery as cq

# Parameters
length = 150
depth = 20
thickness = 10
post_width = 10
post_height = 30
slot_width = 6
slot_height = 5
fillet_radius = 3

# Main beam
beam = cq.Workplane("XY").box(length, depth, thickness)

# End posts
post1 = (
    cq.Workplane("XY")
    .transformed(offset=( length/2 - post_width/2, 0, thickness/2 + post_height/2))
    .box(post_width, depth, post_height)
)
post2 = (
    cq.Workplane("XY")
    .transformed(offset=(-length/2 + post_width/2, 0, thickness/2 + post_height/2))
    .box(post_width, depth, post_height)
)

# Combine beam and posts
handle = beam.union(post1).union(post2)

# Apply fillet to outer edges
handle = handle.edges().fillet(fillet_radius)

# Slot notches at top of posts
slot1 = (
    cq.Workplane("XY")
    .transformed(offset=( length/2 - post_width/2, 0, thickness + post_height - slot_height/2))
    .box(slot_width, depth + 1, slot_height)
)
slot2 = (
    cq.Workplane("XY")
    .transformed(offset=(-length/2 + post_width/2, 0, thickness + post_height - slot_height/2))
    .box(slot_width, depth + 1, slot_height)
)

# Cut slots
result = handle.cut(slot1).cut(slot2)