import cadquery as cq

# Parameters
p1 = (0, 0)
p2 = (100, 0)
p3 = (20, 60)
thickness = 5
wall = 2

# Outer triangular prism
outer = (
    cq.Workplane("XY")
      .polyline([p1, p2, p3])
      .close()
      .extrude(thickness)
)

# Inner cutout prism (slightly smaller triangle)
inner = (
    cq.Workplane("XY")
      .polyline([p1, p2, p3])
      .close()
      .offset2D(-wall)
      .extrude(thickness)
)

# Hollow frame result
result = outer.cut(inner)