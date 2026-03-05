import cadquery as cq

# Define plate thickness
thickness = 5

# 2D outline of the plate
points = [
    (0, 0),
    (40, 0),
    (100, 15),
    (120, 40),
    (90, 80),
    (50, 75),
    (15, 50),
    (0, 15),
]

# Coordinates for larger holes (e.g. 6 mm)
large_hole_positions = [
    (15, 75),
    (35, 75),
    (65, 75),
    (95, 75),
    (115, 60),
    (20, 10),
    (85, 10),
    (55, 45),
]

# Coordinates for smaller holes (e.g. 3 mm)
small_hole_positions = [
    (85, 55),
    (90, 50),
    (95, 45),
    (95, 40),
    (90, 35),
    (85, 30),
]

# Build the model
result = (
    cq.Workplane("XY")
      .polyline(points).close().extrude(thickness)
      .faces(">Z").workplane()
      .pushPoints(large_hole_positions).hole(6)
      .pushPoints(small_hole_positions).hole(3)
)