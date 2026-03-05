import cadquery as cq

# Dimensions (estimated from image)
base_diameter = 40
base_height = 6
post_diameter = 20
post_height = 30
hole_diameter = 8
slot_width = 4
slot_depth = post_height  # slot goes full height of post

# Build base disk
base = (
    cq.Workplane("XY")
    .cylinder(base_height, base_diameter / 2)
)

# Build post on top of base
post = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .cylinder(post_height, post_diameter / 2)
)

# Combine base and post
result = base.union(post)

# Add central through hole
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)

# Cut vertical slot through the post (from top down through post)
# Slot is a rectangular cut from the top going down through the post
slot = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .rect(slot_width, post_diameter + 2)
    .extrude(post_height)
    .translate((0, post_diameter / 2, 0))
)

# Actually make slot go from center outward to edge
slot2 = (
    cq.Workplane("XZ")
    .workplane(offset=0)
)

# Use a box to cut the slot
slot_cut = (
    cq.Workplane("XY")
    .box(slot_width, post_diameter, post_height * 2)
    .translate((0, post_diameter / 4, base_height + post_height / 2))
)

result = result.cut(slot_cut)