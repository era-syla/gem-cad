import cadquery as cq

# Parameters
outer_r = 40
height = 90
wall_thickness = 3
lip_height = 2
lip_overhang = 1
handle_offset = 20
handle_thickness = 6
handle_depth = 10
corner_fillet = 2
z0 = 15
z1 = height - 15

# Create mug body
mug_outer = cq.Workplane("XY").circle(outer_r).extrude(height)
mug_inner = cq.Workplane("XY").circle(outer_r - wall_thickness).extrude(height - wall_thickness)
mug = mug_outer.cut(mug_inner)

# Add interior lip
mug = mug.faces(">Z").workplane().circle(outer_r - lip_overhang).cutBlind(-lip_height)

# Build handle pieces
left_vert = (
    cq.Workplane("XY")
    .box(handle_thickness, handle_depth, z1 - z0)
    .translate((outer_r + handle_thickness / 2, 0, z0 + (z1 - z0) / 2))
)
right_vert = (
    cq.Workplane("XY")
    .box(handle_thickness, handle_depth, z1 - z0)
    .translate((outer_r + handle_offset - handle_thickness / 2, 0, z0 + (z1 - z0) / 2))
)
bottom_horiz = (
    cq.Workplane("XY")
    .box(handle_offset, handle_depth, handle_thickness)
    .translate((outer_r + handle_offset / 2, 0, z0 + handle_thickness / 2))
)
top_horiz = (
    cq.Workplane("XY")
    .box(handle_offset, handle_depth, handle_thickness)
    .translate((outer_r + handle_offset / 2, 0, z1 - handle_thickness / 2))
)

# Combine handle and union with mug
handle = left_vert.union(right_vert).union(bottom_horiz).union(top_horiz)
result = mug.union(handle)

# Fillet handle corners
result = result.edges("|Z or |X").fillet(corner_fillet)