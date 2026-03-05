import cadquery as cq

result = (cq.Workplane("XY")
          .polyline([(0, 0), (50, 30), (100, 0), (0, 0)])
          .close()
          .extrude(10)
          .faces(">Z")
          .workplane()
          .rect(80, 26, forConstruction=True)
          .vertices()
          .cskHole(6, 12, 82)
          .faces("<Z")
          .workplane(invert=True, centerOption='CenterOfBoundBox')
          .center(50, 0)
          .polygon(3, 60)
          .cutBlind(-7))

result = result.edges().fillet(2)