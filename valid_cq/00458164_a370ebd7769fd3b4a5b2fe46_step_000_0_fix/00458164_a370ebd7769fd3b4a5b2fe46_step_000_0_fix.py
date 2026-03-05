import cadquery as cq

result = (
    cq.Workplane("YZ")
      .workplane(offset=0)
      .circle(1)
      .workplane(offset=30)
      .circle(15)
      .workplane(offset=70)
      .circle(2)
      .loft()
)