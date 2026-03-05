import cadquery as cq
import math

length = 120
width = 20
frontH = 20
backH = 10

# Create main tapered prism
result = (
    cq.Workplane("XZ")
      .polyline([(0, 0), (length, 0), (length, backH), (0, frontH)])
      .close()
      .extrude(width)
      .edges().fillet(2)
)

# Cut angled side grooves on both sides
groove_angle = -20  # degrees
for side in ("<Y", ">Y"):
    result = (
        result.faces(side)
              .workplane(origin=(10, 5))
              .transformed(rotate=(0, 0, groove_angle))
              .rect(length - 20, 3)
              .cutThruAll()
    )

# Drill small holes near the front on both sides
for side in ("<Y", ">Y"):
    result = (
        result.faces(side)
              .workplane(origin=(10, 5))
              .hole(4)
    )