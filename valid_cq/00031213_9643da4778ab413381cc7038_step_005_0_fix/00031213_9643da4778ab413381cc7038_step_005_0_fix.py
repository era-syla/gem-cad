import cadquery as cq

# Parameters
base_len = 120.0
base_w = 40.0
base_thk = 3.0
corner_hole_d = 4.0
corner_offset = 5.0
center_hole_d = 10.0
rect_hole_w = 20.0
rect_hole_h = 10.0
rect_hole_offset = -30.0

wall_h = 50.0
wall_thk = base_thk
wall_offset = base_len/2 - wall_thk/2

vert_center_hole_d = 12.0
vert_rect_w = 18.0
vert_rect_h = 10.0

small_hole_d = 4.0
small_hole_offset_y = 10.0
small_hole_offset_z = 15.0

# Build base plate
result = (
    cq.Workplane("XY")
    .box(base_len, base_w, base_thk)
    # Corner holes
    .faces(">Z").workplane()
    .pushPoints([
        (-base_len/2 + corner_offset, -base_w/2 + corner_offset),
        (-base_len/2 + corner_offset,  base_w/2 - corner_offset),
        ( base_len/2 - corner_offset, -base_w/2 + corner_offset),
        ( base_len/2 - corner_offset,  base_w/2 - corner_offset),
    ])
    .circle(corner_hole_d/2).cutThruAll()
    # Center hole
    .faces(">Z").workplane().center(0, 0)
    .circle(center_hole_d/2).cutThruAll()
    # Rectangular cut on left
    .faces(">Z").workplane().center(rect_hole_offset, 0)
    .rect(rect_hole_w, rect_hole_h).cutThruAll()
)

# Add vertical support on right
result = (
    result
    .faces(">Z").workplane().center(wall_offset, 0)
    .rect(wall_thk, base_w).extrude(wall_h)
)

# Cut center round hole in vertical support
result = result.cut(
    cq.Workplane("YZ", origin=(wall_offset + wall_thk/2, 0, base_thk + wall_h/2))
    .circle(vert_center_hole_d/2)
    .extrude(-wall_thk - 1)
)

# Cut rectangular slot in vertical support
result = result.cut(
    cq.Workplane("YZ", origin=(wall_offset + wall_thk/2, 0, base_thk + wall_h - vert_rect_h/2))
    .rect(vert_rect_w, vert_rect_h)
    .extrude(-wall_thk - 1)
)

# Cut two small holes in vertical support
for y_off in (small_hole_offset_y, -small_hole_offset_y):
    result = result.cut(
        cq.Workplane("YZ", origin=(wall_offset + wall_thk/2, y_off, base_thk + small_hole_offset_z))
        .circle(small_hole_d/2)
        .extrude(-wall_thk - 1)
    )