import cadquery as cq

# Parameters
L = 80  # length of the base
H = 50  # height of the back
W = 30  # depth of the prism
r = 5   # fillet radius

# Create a right‐triangle cross‐section and extrude to form a prism
result = (
    cq.Workplane("XY")
      .polyline([(0, 0), (L, 0), (0, H)])
      .close()
      .extrude(W)
      .edges()
      .fillet(r)
)