import cadquery as cq
import math

# Parameters
thickness = 5.0
width = 10.0
hole_diameter = 4.0

L1 = 40.0       # length of first horizontal segment
L2 = 50.0       # length of angled segment
L3 = 40.0       # length of final horizontal segment
angle = 15.0    # angle of the middle segment in degrees

# Compute key points for the centerline
dx = math.cos(math.radians(angle)) * L2
dy = math.sin(math.radians(angle)) * L2

x1, y1 = L1, 0.0
x2, y2 = L1 + dx, dy
x3, y3 = x2 + L3, dy

half_w = width / 2.0

# Outline points (clockwise)
outline = [
    (0.0, -half_w),
    (x1, -half_w),
    (x2, -half_w),
    (x3, -half_w),
    (x3,  half_w),
    (x2,  half_w),
    (x1,  half_w),
    (0.0, half_w),
]

# Hole positions along the centerline
hole_positions = [
    (0.0,   0.0),
    (x1,    0.0),
    ((x1 + x2) / 2.0, (0.0 + y2) / 2.0),
    (x2,    y2),
    (x3,    y3),
]

# Build the part
result = (
    cq.Workplane("XY")
      .polyline(outline)
      .close()
      .extrude(thickness)
      .faces(">Z")
      .workplane()
      .pushPoints(hole_positions)
      .hole(hole_diameter)
)