import cadquery as cq

thk = 5

# create the main plate profile
result = (
    cq.Workplane("XY")
      .polyline([(0, 0), (70, 0)])
      .radiusArc((100, 30), 40)   # curved hook profile
      .lineTo(0, 30)              # top edge back to left
      .close()                    # close profile
      .extrude(thk)               # extrude to thickness
)

# cut the left semicircular notch
result = result.cut(
    cq.Workplane("XY")
      .center(5, 0)
      .circle(5)
      .extrude(thk)
)

# cut the four small rectangular holes
small_hole_centers = [(20, 20), (30, 20), (20, 10), (30, 10)]
result = result.cut(
    cq.Workplane("XY")
      .pushPoints(small_hole_centers)
      .rect(3, 3)
      .extrude(thk)
)

# cut the large curved slot/hook area
result = result.cut(
    cq.Workplane("XY")
      .center(80, 15)
      .circle(15)
      .extrude(thk)
)