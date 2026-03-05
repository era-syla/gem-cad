import cadquery as cq

result = (cq.Workplane("XY")
          .cylinder(50, 5)
          .faces(">Z").workplane()
          .cylinder(100, 3))