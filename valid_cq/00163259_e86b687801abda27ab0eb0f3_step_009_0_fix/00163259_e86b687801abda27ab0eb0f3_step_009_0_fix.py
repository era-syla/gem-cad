import cadquery as cq

# Parameters
width = 60
height = 100
thickness = 5
inset = 20

# Build profile and extrude
result = (
    cq.Workplane("XY")
      .polyline([
          (0, 0),
          (0, height),
          (width, height)
      ])
      .threePointArc((width, 0), (width - inset, 0))
      .close()
      .extrude(thickness)
)