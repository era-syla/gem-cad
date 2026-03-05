import cadquery as cq

# Fuselage via loft of circles along the X-axis
fuselage = (
    cq.Workplane("YZ")
      .workplane(offset=0).circle(0.01)
      .workplane(offset=0.5).circle(0.1)
      .workplane(offset=2.5).circle(0.2)
      .workplane(offset=4.5).circle(0.15)
      .workplane(offset=6.5).circle(0.01)
      .loft()
)

# Main wing: drawn in the X-Z plane and extruded in Y
wing = (
    cq.Workplane("XZ")
      .polyline([(2, -1), (2, 1), (4, 3), (4, -3)])
      .close()
      .extrude(0.05)
      .translate((0, -0.025, 0))
)

# Horizontal tailplane
tail = (
    cq.Workplane("XZ")
      .polyline([(5, -0.5), (5, 0.5), (6, 1.5), (6, -1.5)])
      .close()
      .extrude(0.03)
      .translate((0, -0.015, 0))
)

# Vertical stabilizer: drawn in the X-Y plane and extruded in Z
vstab = (
    cq.Workplane("XY")
      .polyline([(5.8, 0), (5.8, 1.2), (6.1, 1.5), (6.4, 1.2), (6.4, 0)])
      .close()
      .extrude(0.02)
      .translate((0, 0, -0.01))
)

result = fuselage.union(wing).union(tail).union(vstab)