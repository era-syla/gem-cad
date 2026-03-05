import cadquery as cq

# Parameters
thickness = 8.0
foot_offset = 40.0
bar_offset = 20.0
foot_w = 20.0
bar_w = 10.0
big_hole_d = 8.0
small_hole_d = 3.0
text_size = 12.0
text_height = 2.0

half_foot_w = foot_w/2
half_bar_w = bar_w/2

# Define 2D profile
pnts = [
    (-foot_offset, -half_foot_w),
    ( foot_offset, -half_foot_w),
    ( foot_offset,  half_foot_w),
    ( bar_offset,   half_foot_w),
    ( bar_offset,    half_bar_w),
    ( half_bar_w,    half_bar_w),
    ( half_bar_w,    half_foot_w),
    (-half_bar_w,    half_foot_w),
    (-half_bar_w,    half_bar_w),
    (-bar_offset,    half_bar_w),
    (-bar_offset,    half_foot_w),
    (-foot_offset,   half_foot_w),
]

# Build base solid
result = cq.Workplane("XY").polyline(pnts).close().extrude(thickness)

# Large holes through feet and center
for pos in [(-20, 0), (20, 0), (0, 0)]:
    result = result.faces(">Z").workplane().pushPoints([pos]).hole(big_hole_d)

# Small side holes on left and right faces
result = result.faces("<X").workplane().hole(small_hole_d)
result = result.faces(">X").workplane().hole(small_hole_d)

# Embossed letter B on top face
result = result.faces(">Z").workplane().text("B", text_size, text_height, font="Arial")

# The variable 'result' now contains the finished solid geometry.