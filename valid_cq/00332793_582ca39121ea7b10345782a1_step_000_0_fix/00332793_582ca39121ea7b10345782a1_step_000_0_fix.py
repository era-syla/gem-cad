import cadquery as cq

result = (cq.Workplane("XY")
          .moveTo(0, 0).lineTo(10, 0).lineTo(20, 10).lineTo(15, 50).lineTo(5, 60).lineTo(0, 50).close()
          .extrude(5)
          .faces(">Z").workplane()
          .center(5, 5).hole(2)
          .center(0, 40).hole(2)
          .center(10, -10).hole(2)
          .center(5, -40).hole(2)
          .center(-10, 10).hole(2))