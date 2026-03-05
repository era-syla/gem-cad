import cadquery as cq
import math

# Parameters
rad = 10        # radius of semicircle
rect_len = 20   # length of rectangular part before semicircle
depth = 40      # extrusion depth (length of block)
big_dia = 14    # diameter of large hole
small_dia = 6   # diameter of small hole
small_off_x = rect_len * 0.5
small_off_y = -rad * 0.5

# Build profile: rectangle + semicircle
profile = (
    cq.Workplane("XY")
    .moveTo(0, -rad)
    .lineTo(rect_len, -rad)
    .threePointArc((rect_len + rad, 0), (rect_len, rad))
    .lineTo(0, rad)
    .close()
)

# Extrude profile
result = profile.extrude(depth)

# Cut the large hole through the semicircular region
result = (
    result
    .faces(">Z")
    .workplane()
    .center(rect_len, 0)
    .hole(big_dia)
)

# Cut the smaller hole
result = (
    result
    .faces(">Z")
    .workplane()
    .center(small_off_x, small_off_y)
    .hole(small_dia)
)