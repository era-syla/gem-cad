import cadquery as cq

major_radius = 50
tube_radius = 2

result = (
    cq.Workplane("XZ")
      .center(major_radius, 0)
      .circle(tube_radius)
      .revolve(360, axisStart=(0, 0, 0), axisEnd=(0, 0, 1))
)