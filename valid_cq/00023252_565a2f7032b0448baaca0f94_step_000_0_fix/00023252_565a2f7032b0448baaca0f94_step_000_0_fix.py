import cadquery as cq
import math

# Parameters
L = 160.0      # total length
w = 15.0       # width
r = w / 2      # end radius
thick = 4.0    # plate thickness
d_mid = 2.5    # diameter of middle holes
d_end = 3.0    # diameter of end holes

# Create the capsule-shaped plate
part = (
    cq.Workplane("XY")
    .moveTo(L/2 - r,  w/2)
    .lineTo(-L/2 + r, w/2)
    .threePointArc((-L/2, 0),   (-L/2 + r, -w/2))
    .lineTo(L/2 - r, -w/2)
    .threePointArc((L/2, 0),    (L/2 - r,  w/2))
    .close()
    .extrude(thick)
)

# Prepare hole locations
pts_mid = []
# Two rows of holes along the bar
n_mid = 11
start_x = -60.0
spacing = 12.0
y_off = 4.0
for i in range(n_mid):
    x = start_x + i * spacing
    pts_mid.append((x,  y_off))
    pts_mid.append((x, -y_off))

pts_end = []
# Circular hole patterns at each end
for side in (-1, 1):
    cx = side * (L/2)
    # Outer ring
    for i in range(8):
        angle = i * 360.0 / 8.0
        rad = r - 2.0
        pts_end.append((cx + math.cos(math.radians(angle)) * rad,
                        math.sin(math.radians(angle)) * rad))
    # Inner ring
    for i in range(5):
        angle = i * 360.0 / 5.0
        rad = r - 4.0
        pts_end.append((cx + math.cos(math.radians(angle)) * rad,
                        math.sin(math.radians(angle)) * rad))

# Drill holes
result = (
    part
    .faces(">Z").workplane()
    .pushPoints(pts_mid).hole(d_mid)
    .pushPoints(pts_end).hole(d_end)
)