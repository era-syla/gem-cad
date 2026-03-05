import cadquery as cq

# Parameters
depth = 10  # extrusion depth in Z
# 2D profile points in the X-Y plane
profile = [
    (-10, 0),
    (10, 0),
    (5, 5),
    (5, 20),
    (-5, 20),
    (-5, 5),
]

result = (
    cq.Workplane("XY")
      .polyline(profile)
      .close()
      .extrude(depth)
)