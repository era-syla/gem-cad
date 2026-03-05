import cadquery as cq

thickness = 5.0
fillet_radius = 2.0
hole_diameter = 6.0

# define the 2D outline of the plate
points = [
    (0, 0),
    (120, 0),
    (150, 50),
    (100, 80),
    (0, 80)
]

# build the plate, extrude, and fillet all outer edges
result = (
    cq.Workplane("XY")
      .polyline(points)
      .close()
      .extrude(thickness)
      .edges()
      .fillet(fillet_radius)
)

# hole coordinates on the top face
hole_positions = [
    (10, 10),
    (45, 10),
    (80, 10),
    (115, 10),
    (30, 70),
    (70, 70),
    (110, 70),
    (60, 40)
]

# drill through holes at each position
for x, y in hole_positions:
    result = (
        result
          .faces(">Z")
          .workplane(offset=0)
          .pushPoints([(x, y)])
          .hole(hole_diameter)
    )