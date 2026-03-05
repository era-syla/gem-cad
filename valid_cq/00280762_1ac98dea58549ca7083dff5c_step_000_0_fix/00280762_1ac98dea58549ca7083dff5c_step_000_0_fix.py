import cadquery as cq

# Parameters
L_end = 20
L_trans = 20
L_neck = 20
H1 = 10
H2 = 4
thickness = 10

# Compute key X positions
x0 = 0
x1 = L_end
x2 = x1 + L_trans
x3 = x2 + L_neck
x4 = x3 + L_trans
x5 = x4 + L_end

# Define top profile polyline
pts = [
    (x0, 0),
    (x5, 0),
    (x5, H1),
    (x4, H1),
    (x3, H2),
    (x2, H2),
    (x1, H1),
    (x0, H1),
]

# Build the solid
result = (
    cq.Workplane("XY")
      .polyline(pts)
      .close()
      .extrude(thickness)
)