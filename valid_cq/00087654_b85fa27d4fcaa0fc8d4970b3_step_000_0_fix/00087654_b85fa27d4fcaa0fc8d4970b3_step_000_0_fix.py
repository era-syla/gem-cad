import cadquery as cq

# Create the base shape
result = (cq.Workplane("XY")
          .circle(10).extrude(2)
          .faces(">Z")
          .workplane()
          .circle(4).cutThruAll())

# Create the main body
result = (result.faces(">Z")
          .workplane()
          .moveTo(0, 0)
          .rect(20, 30)
          .extrude(10))

# Create the tapered arm
result = (result.faces(">Z")
          .workplane()
          .moveTo(15, 0)
          .lineTo(70, 0).lineTo(55, 20).close()
          .extrude(8))

# Chamfer the edge
result = result.edges("|Z").chamfer(1)