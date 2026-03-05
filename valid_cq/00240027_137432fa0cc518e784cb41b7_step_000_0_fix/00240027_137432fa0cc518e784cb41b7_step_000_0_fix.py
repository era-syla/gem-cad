import cadquery as cq

result = (cq.Workplane("XY")
          .rect(40, 10, forConstruction=True)
          .vertices()
          .circle(5)
          .extrude(3)
          .faces(">Z")
          .workplane()
          .rarray(10, 1, 4, 1)
          .circle(2)
          .cutThruAll())