import cadquery as cq

# Define the handle
handle = (cq.Workplane("XY")
          .lineTo(60, 0)
          .radiusArc((80, 20), -20)
          .lineTo(90, 80)
          .radiusArc((60, 100), -20)
          .lineTo(0, 100)
          .close()
          .extrude(5))

# Define the fork
fork = (cq.Workplane("XY")
        .center(0, 100)
        .rect(80, 40)
        .extrude(5)
        .faces(">Z")
        .workplane()
        .pushPoints([(-30, 0), (0, 0), (30, 0)])
        .slot2D(30, 10)
        .cutThruAll())

# Combine handle and fork
result = handle.union(fork)

# Add a text label
result = (result.faces("<Z")
          .workplane(centerOption="CenterOfBoundBox", invert=True)
          .text("SPOON", 10, 1, cut=True, combine=False))