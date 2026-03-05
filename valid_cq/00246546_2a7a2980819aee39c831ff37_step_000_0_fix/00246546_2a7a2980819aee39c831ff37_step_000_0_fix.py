import cadquery as cq

# Parameters
base_length = 100
base_width = 50
top_length = 80
top_width = 30
height = 20
fillet_radius = 3

result = (
    cq.Workplane("XY")
      .rect(base_length, base_width)
      .workplane(offset=height)
      .rect(top_length, top_width)
      .loft()
      .edges().fillet(fillet_radius)
)