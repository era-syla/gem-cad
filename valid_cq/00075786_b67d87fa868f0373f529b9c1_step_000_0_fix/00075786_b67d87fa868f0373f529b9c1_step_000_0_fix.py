import cadquery as cq

# Parameters
L = 100     # total length
T = 5       # top bar thickness
D = 20      # leg drop height
R = 15      # corner fillet radius
W = 10      # extrusion width (Y direction)
A = 10      # arch radius
num = 4     # number of arches

# Create outer profile and extrude
result = (
    cq.Workplane("XZ")
      .moveTo(0, 0)
      .lineTo(0, D)
      .radiusArc((R, D + T), R)
      .lineTo(L - R, D + T)
      .radiusArc((L, D), R)
      .lineTo(L, 0)
      .close()
      .extrude(W)
)

# Cut out the evenly spaced arches
for i in range(1, num + 1):
    xi = R + (L - 2 * R) * i / (num + 1)
    cutter = (
        cq.Workplane("XZ")
          .moveTo(xi, A)
          .circle(A)
          .extrude(W + 2)
    )
    result = result.cut(cutter)