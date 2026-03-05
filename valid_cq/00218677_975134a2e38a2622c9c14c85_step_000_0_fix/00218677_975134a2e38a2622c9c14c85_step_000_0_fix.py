import cadquery as cq

result = (cq.Workplane("XY")
          .rect(30, 10)
          .extrude(3)
          .edges("|Z")
          .fillet(2)
          .faces(">Z")
          .workplane()
          .pushPoints([(-10, 0), (10, 0)])
          .circle(3)
          .cutBlind(-3))