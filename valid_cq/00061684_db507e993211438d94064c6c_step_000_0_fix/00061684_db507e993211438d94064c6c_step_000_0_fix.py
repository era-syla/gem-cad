import cadquery as cq

# Parameters
L = 100    # length of the triangle legs
T = 12     # overall thickness in Z
off = 15   # offset of the inner cut from the edges
cutD = 8   # depth of the inner pocket
r = 3      # fillet radius on vertical edges

# Build outer triangular prism
result = (
    cq.Workplane("XY")
      .polyline([(0, 0), (L, 0), (0, L)])
      .close()
      .extrude(T)
)

# Cut an inner, similar triangle pocket
result = (
    result
      .faces(">Z")
      .workplane()
      .polyline([(off, off), (L-off, off), (off, L-off)])
      .close()
      .cutBlind(-cutD)
)

# Fillet all vertical edges (outer and pocket)
result = result.edges("|Z").fillet(r)