import cadquery as cq

result = (cq.Workplane("XY")
          .box(40, 20, 2)
          .faces(">Z")
          .workplane()
          .rarray(15, 1, 3, 1)
          .circle(2.5)
          .extrude(10)
          .edges("|Z")
          .fillet(1))

result