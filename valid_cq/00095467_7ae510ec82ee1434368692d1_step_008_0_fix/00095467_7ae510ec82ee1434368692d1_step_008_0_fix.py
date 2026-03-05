import cadquery as cq

radius = 10
length = 40
height = 80
rect_length = length - 2*radius

result = (
    cq.Workplane("XY")
      .rect(rect_length, 2*radius)
      .moveTo(rect_length/2, 0).circle(radius)
      .moveTo(-rect_length/2, 0).circle(radius)
      .extrude(height)
)