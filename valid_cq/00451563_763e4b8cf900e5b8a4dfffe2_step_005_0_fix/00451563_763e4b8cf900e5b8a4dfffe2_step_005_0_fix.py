import cadquery as cq

L = 100.0
w_end = 40.0
w_mid = 20.0
cut = 15.0
thickness = 3.0

center_dia = 20.0
small_dia = 6.0
large_dia = 10.0

hole_x = L/2 - cut - 10.0
hole_y = w_end/2 - 8.0

result = (
    cq.Workplane("XY")
      .polyline([
          (-L/2,  w_end/2),
          (-L/2 + cut, w_mid/2),
          ( L/2 - cut, w_mid/2),
          ( L/2,  w_end/2),
          ( L/2, -w_end/2),
          ( L/2 - cut, -w_mid/2),
          (-L/2 + cut, -w_mid/2),
          (-L/2, -w_end/2)
      ])
      .close()
      .extrude(thickness)
      .faces(">Z")
      .workplane()
      .pushPoints([(0, 0)])
      .hole(center_dia)
      .pushPoints([(-hole_x, hole_y), (hole_x, hole_y)])
      .hole(small_dia)
      .pushPoints([(-hole_x, -hole_y), (hole_x, -hole_y)])
      .hole(large_dia)
)
