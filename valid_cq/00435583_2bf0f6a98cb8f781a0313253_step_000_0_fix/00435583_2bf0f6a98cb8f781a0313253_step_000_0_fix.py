import cadquery as cq

result = (cq.Workplane("XY")
          .circle(10)
          .workplane(offset=20)
          .circle(5)
          .loft()
          .faces(">Z")
          .workplane()
          .circle(5)
          .sphere(5)
          )