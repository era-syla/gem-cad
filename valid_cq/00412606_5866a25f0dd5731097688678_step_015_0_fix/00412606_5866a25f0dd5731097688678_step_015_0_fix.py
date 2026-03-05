import cadquery as cq

# Base plate
base = (
    cq.Workplane("XY")
      .rect(60, 20)
      .extrude(5)
      .edges("|Z")
      .fillet(5)
)

# Vertical fin
fin = (
    cq.Workplane("XZ", origin=(0, 10, 5))
      .moveTo(0, 0)
      .lineTo(0, 40)
      .threePointArc((10, 45), (20, 40))
      .lineTo(20, 0)
      .close()
      .extrude(10)
      .edges()
      .fillet(2)
)

# Bottom pin
pin = (
    cq.Workplane("XY")
      .circle(3)
      .extrude(5)
)

# Combine base, fin, and pin
result = base.union(fin).union(pin)

# Hole through the fin near the top
result = (
    result.faces(">Y")
      .workplane()
      .center(10, 40)
      .circle(4)
      .cutThruAll()
)

# Emboss text "35" on the fin face
result = (
    result.faces(">Y")
      .workplane()
      .center(10, 20)
      .text("35", 8, 1)
)