import cadquery as cq

# Parameters
big_R = 30
small_R = 15
shaft_len = 100
big_bore = 20
small_bore = 8
fillet_rad = 2

# Create the rod by lofting between two circles
rod = (
    cq.Workplane("XY")
      .circle(big_R)
      .workplane(offset=shaft_len)
      .circle(small_R)
      .loft()
)

# Cut out the big-end bore
hole1 = (
    cq.Workplane("XY")
      .circle(big_bore)
      .extrude(shaft_len + 10)
)

# Cut out the small-end bore
hole2 = (
    cq.Workplane("XY")
      .workplane(offset=shaft_len)
      .circle(small_bore)
      .extrude(shaft_len + 10)
)

# Subtract bores and fillet edges
result = (
    rod
      .cut(hole1)
      .cut(hole2)
      .edges()
      .fillet(fillet_rad)
)