import cadquery as cq
import math

# Build bottle body using revolve
# Profile: wider at bottom, narrowing to neck at top
# Points define half-profile (right side) from bottom to top

bottle_profile = [
    (0, 0),       # bottom center
    (18, 0),      # bottom edge
    (22, 5),      # lower bulge
    (24, 20),     # widest point
    (23, 40),     # upper body
    (18, 60),     # shoulder start
    (10, 72),     # shoulder
    (8, 78),      # neck bottom
    (8, 85),      # neck top
    (0, 85),      # top center
]

# Create bottle body by revolving profile
bottle = (
    cq.Workplane("XZ")
    .polyline(bottle_profile)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# Create neck/thread area cylinder
neck_outer = 10
neck_height = 85
neck_top = 92

# Cap base (flat disk wider than neck)
cap_base_r = 14
cap_base_h = 4

cap_base = (
    cq.Workplane("XY")
    .workplane(offset=neck_height)
    .circle(cap_base_r)
    .extrude(cap_base_h)
)

# Cap top (slightly smaller cylinder)
cap_top = (
    cq.Workplane("XY")
    .workplane(offset=neck_height + cap_base_h)
    .circle(cap_base_r - 1)
    .extrude(3)
)

# Combine cap parts
cap = cap_base.union(cap_top)

# Add knurling to cap using vertical ribs
num_ribs = 24
rib_w = 1.5
rib_depth = 1.2
rib_h = cap_base_h + 3

ribs = None
for i in range(num_ribs):
    angle = i * (360.0 / num_ribs)
    angle_rad = math.radians(angle)
    x = (cap_base_r - 0.5) * math.cos(angle_rad)
    y = (cap_base_r - 0.5) * math.sin(angle_rad)
    
    rib = (
        cq.Workplane("XY")
        .workplane(offset=neck_height)
        .center(x, y)
        .rect(rib_w, rib_depth)
        .extrude(rib_h)
    )
    if ribs is None:
        ribs = rib
    else:
        ribs = ribs.union(rib)

if ribs is not None:
    cap = cap.union(ribs)

# Combine bottle and cap
result = bottle.union(cap)