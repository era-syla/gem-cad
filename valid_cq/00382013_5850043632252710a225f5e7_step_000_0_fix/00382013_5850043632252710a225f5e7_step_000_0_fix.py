import cadquery as cq

result = (cq.Workplane("XY")
          .rect(100, 150)
          .extrude(5)
          .edges("|Z")
          .fillet(5))