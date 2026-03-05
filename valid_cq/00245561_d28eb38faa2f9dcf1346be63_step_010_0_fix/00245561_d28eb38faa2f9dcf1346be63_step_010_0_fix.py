import cadquery as cq

result = (cq.Workplane("XY")
          .box(40, 40, 5)
          .edges("|Z").fillet(3)
          .faces(">Z").workplane()
          .text("XS", fontsize=20, distance=1, cut=True)
          .faces("<Z").workplane()
          .circle(3).cutBlind(-5))