import cadquery as cq
import math

rod_radius = 1.0
lower_height = 80.0
upper_height = 20.0
spacing = 2.2

# positions: center plus 6 around in a hexagon
angles = [i * 60 for i in range(6)]
positions = [(spacing * math.cos(math.radians(a)), spacing * math.sin(math.radians(a))) for a in angles]
positions.insert(0, (0, 0))

result = (
    cq.Workplane("XY")
      .pushPoints(positions)
      .circle(rod_radius)
      .extrude(lower_height)
      .faces(">Z")
      .workplane()
      .circle(rod_radius)
      .extrude(upper_height)
)