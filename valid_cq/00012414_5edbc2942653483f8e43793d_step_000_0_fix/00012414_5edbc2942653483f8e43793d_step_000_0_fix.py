import cadquery as cq

# Base shape
result = (cq.Workplane("XY")
          .lineTo(15, 0)
          .lineTo(30, 20)
          .lineTo(20, 100)
          .lineTo(0, 120)
          .close()
          .extrude(5))

# Holes
result = (result.faces(">Z")
          .workplane()
          .pushPoints([(10, 10), (25, 45), (15, 95), (5, 115)])
          .hole(5))