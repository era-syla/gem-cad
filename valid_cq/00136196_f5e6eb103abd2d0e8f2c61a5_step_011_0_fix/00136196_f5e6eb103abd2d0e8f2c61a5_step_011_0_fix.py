import cadquery as cq

# Define plate outline vertices
outline = [(-40, -20), (40, -20), (55, 0), (0, 50), (-55, 0)]
# Define hole center positions
hole_positions = [(-30, -15), (30, -15), (0, 0), (30, 20), (-30, 20)]

result = (
    cq.Workplane("XY")
      .polyline(outline).close().extrude(5)
      .faces(">Z").workplane()
      .pushPoints(hole_positions).hole(8)
)