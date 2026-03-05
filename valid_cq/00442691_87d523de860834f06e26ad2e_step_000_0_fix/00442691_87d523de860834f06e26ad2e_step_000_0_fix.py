import cadquery as cq

# Approximate control points for a treble clef curve in the XY plane
points = [
    (0, 0),
    (5, 20),
    (2, 45),
    (10, 60),
    (20, 55),
    (15, 35),
    (16, 15),
    (14, 5),
    (10, 2),
    (6, 5),
    (3, 3),
    (0, 0)
]

thickness = 3    # Extrusion thickness in Z
half_width = 2   # Half of the desired line width of the clef
hole_diameter = 4

# Build the clef profile: a spline, closed into a wire, offset to give it width, then extruded
result = (
    cq.Workplane("XY")
      .spline(points)
      .close()
      .wires()
      .offset2D(half_width)
      .extrude(thickness)
      # Add the small circular hole at the tail end (first point)
      .faces(">Z")
      .workplane()
      .center(points[0][0], points[0][1])
      .hole(hole_diameter)
)