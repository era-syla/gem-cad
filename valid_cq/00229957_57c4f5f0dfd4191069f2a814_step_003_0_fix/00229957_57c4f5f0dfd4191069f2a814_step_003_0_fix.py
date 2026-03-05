import cadquery as cq
import math

# Parameters
OD = 100.0                # outer diameter
frame_th = 5.0            # ring thickness
rod_w = 3.0               # rod width
rod_h = 5.0               # rod height
spacing = 10.0            # center-to-center spacing of rods
angle = 45.0              # rod angle in degrees

# Create outer ring (frame)
frame = (
    cq.Workplane("XY")
      .circle(OD/2)
      .circle(OD/2 - frame_th)
      .extrude(rod_h)
)

# Create a grid of rectangular rods
# Use a length that definitely covers the circular area when rotated
rod_length = OD * 1.5
# Compute how many rods we need on each side of center
count = int((OD/2) / spacing) + 2

rods = cq.Workplane("XY")
for i in range(-count, count + 1):
    rods = rods.union(
        cq.Workplane("XY")
          .box(rod_length, rod_w, rod_h)
          .translate((0, i * spacing, rod_h/2))
    )

# Rotate rods to desired angle
rods = rods.rotate((0, 0, 0), (0, 0, 1), angle)

# Clip rods to the inner circle of the ring
clipper = cq.Workplane("XY").circle(OD/2 - frame_th).extrude(rod_h)
rods = rods.intersect(clipper)

# Combine frame and rods
result = frame.union(rods)