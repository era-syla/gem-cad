import cadquery as cq

length = 100.0
width_start = 20.0
height_start = 10.0
width_end = 5.0
height_end = 2.0
tip_radius = 1.0

result = (
    cq.Workplane("YZ")
      .rect(width_start, height_start)
      .workplane(offset=length)
      .rect(width_end, height_end)
      .loft()
      .faces(">X")
      .edges()
      .fillet(tip_radius)
)