import cadquery as cq

# Parameters
width = 30
length = 100
height_front = 10
height_back = 20
fillet_radius = 2

# Build the side profile and extrude
result = (
    cq.Workplane("XZ")
      .polyline([
          (0, 0),
          (length, 0),
          (length, height_front),
          (0, height_back)
      ])
      .close()
      .extrude(width)
      .edges("|X or |Y")
      .fillet(fillet_radius)
)