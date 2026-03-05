import cadquery as cq

radius = 25
length = radius
thickness = 5

result = (
    cq.Workplane("XY")
      .moveTo(0, -radius)
      .lineTo(length, -radius)
      .lineTo(length, radius)
      .threePointArc((2*radius, 0), (length, -radius))
      .close()
      .extrude(thickness)
)