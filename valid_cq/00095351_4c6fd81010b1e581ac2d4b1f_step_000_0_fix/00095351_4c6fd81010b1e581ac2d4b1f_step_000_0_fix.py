import cadquery as cq

# Parameters
L, W, H, T = 200, 60, 60, 2

result = (
    cq.Workplane("XY")
    # Outer box
    .box(L, W, H)
    # Hollow and open the front (-X) face
    .faces("<X").shell(-T)
    # Top face operations
    .faces(">Z").workplane()
    # Small circular hole near front
    .pushPoints([(-L/2 + 20, 0)]).hole(4)
    # Three small rectangular slots in middle
    .pushPoints([(-L/2 + 70, -10), (-L/2 + 70, 0), (-L/2 + 70, 10)])
    .rect(6, 3).cutThruAll()
    # Large hole near rear
    .pushPoints([(L/2 - 30, 0)]).hole(20)
    # Side holes (one on each side at center)
    .faces(">Y").workplane().hole(3)
    .faces("<Y").workplane().hole(3)
    # Two mounting holes on back face (+X)
    .faces(">X").workplane()
    .pushPoints([(0, 10), (0, -10)]).hole(4)
)

# 'result' now contains the final solid geometry.