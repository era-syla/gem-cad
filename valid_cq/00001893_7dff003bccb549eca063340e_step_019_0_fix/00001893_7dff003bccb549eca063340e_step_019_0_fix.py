import cadquery as cq

thickness = 10.0
# Define the organic main profile in the XY plane
profile_pts = [
    (0, 30),
    (20, 35),
    (40, 20),
    (35, 0),
    (20, -30),
    (0, -40),
    (-30, -30),
    (-35, 0),
    (-20, 20),
    (-5, 35),
]

# Create the main body by extruding the closed profile
body = (
    cq.Workplane("XY")
    .polyline(profile_pts)
    .close()
    .extrude(thickness)
)

# Subtract a through‐cut cylinder on the left side
cut_radius = 15.0
cut_center = (-25, 0)
body = body.cut(
    cq.Workplane("XY")
    .workplane(offset=thickness / 2)
    .center(cut_center[0], cut_center[1])
    .circle(cut_radius)
    .extrude(thickness)
)

# Add two small bosses on the lower right "leaf" extension
boss_radius = 3.0
boss_height = 5.0
boss_center = (20, -20)
boss_top = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .center(boss_center[0], boss_center[1])
    .circle(boss_radius)
    .extrude(boss_height)
)
boss_bottom = (
    cq.Workplane("XY")
    .workplane()
    .center(boss_center[0], boss_center[1])
    .circle(boss_radius)
    .extrude(-boss_height)
)

# Fuse all parts into the final result
result = body.union(boss_top).union(boss_bottom)