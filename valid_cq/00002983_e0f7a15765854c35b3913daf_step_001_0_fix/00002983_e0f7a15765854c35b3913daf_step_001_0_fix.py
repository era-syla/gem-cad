import cadquery as cq

L = 100
D = 20
H = 20
R = 10

result = cq.Workplane("XY").box(L, D, H, centered=(False, True, False))

# left bottom quarter‐cylinder cut
result = result.cut(
    cq.Workplane("XZ")
      .transformed(offset=(0, -D, 0))
      .circle(R)
      .extrude(2 * D)
)

# right top quarter‐cylinder cut
result = result.cut(
    cq.Workplane("XZ")
      .transformed(offset=(L, -D, H))
      .circle(R)
      .extrude(2 * D)
)