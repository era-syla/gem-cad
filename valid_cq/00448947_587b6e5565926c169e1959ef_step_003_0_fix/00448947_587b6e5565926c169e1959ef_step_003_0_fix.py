import cadquery as cq

outer_radius = 50
cross_section_radius = 3

result = (
    cq.Workplane("XZ")
      .center(outer_radius, 0)
      .circle(cross_section_radius)
      .revolve(360, (0, 0, 0), (0, 0, 1))
)