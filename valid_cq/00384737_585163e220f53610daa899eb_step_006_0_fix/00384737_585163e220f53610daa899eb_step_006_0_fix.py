import cadquery as cq

length = 200.0
width = 20.0
height = 10.0
thickness = 2.0
hole_diameter = 5.0

pts = [
    (-width/2, 0),
    (-width/2, height),
    (width/2, height),
    (width/2, 0),
    (thickness/2, 0),
    (thickness/2, height - thickness),
    (-thickness/2, height - thickness),
    (-thickness/2, 0),
]

result = (
    cq.Workplane("YZ")
      .polyline(pts)
      .close()
      .extrude(length)
      .faces(">X")
      .workplane()
      .hole(hole_diameter)
)