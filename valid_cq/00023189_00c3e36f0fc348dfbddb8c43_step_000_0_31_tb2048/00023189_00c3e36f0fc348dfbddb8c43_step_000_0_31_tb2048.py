import cadquery as cq

# Parametric dimensions
width = 36.0
height = 36.0
length = 320.0
thickness = 2.0

hole_pitch = 16.0
large_hole_dia = 8.0
small_hole_dia = 4.0
pattern_offset = 6.0

# Create base U-channel
result = (
    cq.Workplane("XY")
    .box(width, length, height)
    .faces(">Z")
    .shell(-thickness)
)

num_holes = int(length // hole_pitch)

# --- Web Cutters (Cut along Z axis) ---
# XY plane: local X is global X, local Y is global Y
large_pts_xy = [(0, (i - num_holes/2 + 0.5) * hole_pitch) for i in range(num_holes)]
small_pts_xy = []
for p in large_pts_xy:
    small_pts_xy.extend([
        (p[0] + pattern_offset, p[1] + pattern_offset),
        (p[0] - pattern_offset, p[1] + pattern_offset),
        (p[0] + pattern_offset, p[1] - pattern_offset),
        (p[0] - pattern_offset, p[1] - pattern_offset),
    ])

web_cutter = (
    cq.Workplane("XY")
    .pushPoints(large_pts_xy).circle(large_hole_dia / 2)
    .pushPoints(small_pts_xy).circle(small_hole_dia / 2)
    .extrude(height)
)
web_cutter2 = (
    cq.Workplane("XY")
    .pushPoints(large_pts_xy).circle(large_hole_dia / 2)
    .pushPoints(small_pts_xy).circle(small_hole_dia / 2)
    .extrude(-height)
)

result = result.cut(web_cutter).cut(web_cutter2)

# --- Flange Cutters (Cut along X axis) ---
# YZ plane: local X is global Y, local Y is global Z
large_pts_yz = [((i - num_holes/2 + 0.5) * hole_pitch, 0) for i in range(num_holes)]
small_pts_yz = []
for p in large_pts_yz:
    small_pts_yz.extend([
        (p[0] + pattern_offset, p[1] + pattern_offset),
        (p[0] - pattern_offset, p[1] + pattern_offset),
        (p[0] + pattern_offset, p[1] - pattern_offset),
        (p[0] - pattern_offset, p[1] - pattern_offset),
    ])

flange_cutter = (
    cq.Workplane("YZ")
    .pushPoints(large_pts_yz).circle(large_hole_dia / 2)
    .pushPoints(small_pts_yz).circle(small_hole_dia / 2)
    .extrude(width)
)
flange_cutter2 = (
    cq.Workplane("YZ")
    .pushPoints(large_pts_yz).circle(large_hole_dia / 2)
    .pushPoints(small_pts_yz).circle(small_hole_dia / 2)
    .extrude(-width)
)

result = result.cut(flange_cutter).cut(flange_cutter2)