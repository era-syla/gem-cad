import cadquery as cq

# Parameters
t_top = 5        # top plate thickness
h_web = 10       # web height
t_bottom = 5     # bottom flange thickness
L = 100          # total length in X
x0 = 60          # start of bottom flange/web in X
depth = 20       # extrusion depth in Y

# Build the cross‐section in the XZ‐plane
pts = [
    (0, t_top + h_web + t_bottom),
    (L, t_top + h_web + t_bottom),
    (L, t_bottom),
    (x0, t_bottom),
    (x0, h_web + t_bottom),
    (0, h_web + t_bottom),
]

# Extrude the profile along Y to make the 3D solid
result = (
    cq.Workplane("XZ")
      .polyline(pts)
      .close()
      .extrude(depth)
)