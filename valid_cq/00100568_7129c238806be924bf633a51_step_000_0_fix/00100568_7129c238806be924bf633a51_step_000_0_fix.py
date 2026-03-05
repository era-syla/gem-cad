import cadquery as cq

# Parameters
thk = 5.0      # plate thickness
w = 15.0       # plate width
L1 = 50.0      # horizontal leg length
L2 = 80.0      # vertical leg length
m = 7.5        # miter offset
d_hole = 5.0   # hole diameter

# Horizontal leg
horiz = cq.Workplane("XY").rect(L1, w, centered=(False, True)).extrude(thk)

# Vertical leg
vert = (
    cq.Workplane("XY")
    .transformed(offset=(L1, 0, 0))
    .rect(w, L2, centered=(False, False))
    .extrude(thk)
)

# Union legs
result = horiz.union(vert)

# Cut inside miter (triangular prism)
cut = (
    cq.Workplane("XY")
    .polyline([(L1 - m, 0), (L1, m), (L1 - m, m)])
    .close()
    .extrude(thk)
)
result = result.cut(cut)

# Add holes: one at end of horizontal, three on vertical leg
hole_positions = [
    (L1 - d_hole / 2, 0),
    (L1 + w / 2, 15),
    (L1 + w / 2, 40),
    (L1 + w / 2, 65),
]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(d_hole, thk)
)