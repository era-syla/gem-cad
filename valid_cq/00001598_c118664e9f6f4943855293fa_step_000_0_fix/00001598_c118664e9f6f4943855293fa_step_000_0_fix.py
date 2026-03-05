import cadquery as cq

# Define profile points in the XZ-plane (radius, height)
profile = [
    (0, 0),
    (20, 0),   # bottom outer radius = 20
    (20, 10),  # height 10
    (18, 10),  # step down to radius 18
    (18, 12),  # height 2
    (15, 12),  # step down to radius 15
    (15, 30),  # height 18
    (10, 30),  # step down to radius 10
    (10, 40),  # height 10
    (8, 40),   # step down to radius 8
    (8, 50),   # height 10
    (0, 50)    # close at centerline
]

result = (
    cq.Workplane("XZ")
      .polyline(profile)
      .close()
      .revolve(360)
)

result