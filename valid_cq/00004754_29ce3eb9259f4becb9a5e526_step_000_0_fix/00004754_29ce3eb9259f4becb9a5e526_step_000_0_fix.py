import cadquery as cq

# parameters
radius = 10
height = 60
twist_angle = 90

# create twisted cylinder by lofting between two rotated circles
result = (
    cq.Workplane("XY")
      .circle(radius)
      .workplane(offset=height)
      .transformed(rotate=(0, 0, twist_angle))
      .circle(radius)
      .loft()
)