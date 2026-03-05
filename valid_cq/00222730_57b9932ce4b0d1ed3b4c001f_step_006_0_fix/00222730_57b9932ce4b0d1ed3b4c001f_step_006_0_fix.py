import cadquery as cq

# Base bar
result = cq.Workplane("XY").box(150, 20, 10)

# Top rectangular feature
result = result.union(
    cq.Workplane("XY")
      .transformed(offset=(30, 0, 10))
      .box(60, 20, 12)
)

# Raised middle block
result = result.union(
    cq.Workplane("XY")
      .transformed(offset=(90, 0, 10))
      .box(15, 20, 18)
)

# Small front block
result = result.union(
    cq.Workplane("XY")
      .transformed(offset=(135, 0, 10))
      .box(12, 20, 8)
)

# Top slot pocket
result = result.faces(">Z").workplane().transformed(offset=(50, 0, 6)).rect(50, 8).cutBlind(-5)

# Side notch pocket on the positive X face
result = result.faces(">X").workplane().transformed(offset=(85, 0, 9)).rect(20, 12).cutBlind(-7)

# Chamfer all leading edges on the positive X side
result = result.edges(">X").chamfer(1)