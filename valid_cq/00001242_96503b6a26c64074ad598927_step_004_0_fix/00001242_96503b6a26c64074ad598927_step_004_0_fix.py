import cadquery as cq

th = 1.0
Wb = 6.0
Wn = 3.0
L1 = 10.0
L2 = 10.0
L3 = 60.0

# 2D profile points in the XY plane
pts = [
    (0,   Wb/2),
    (L1,  Wb/2),
    (L1,  Wn/2),
    (L1+L2, Wn/2),
    (L1+L2+L3, 0),
    (L1+L2, -Wn/2),
    (L1,  -Wn/2),
    (L1,  -Wb/2),
    (0,   -Wb/2)
]

# Create the blade profile and extrude
result = (
    cq.Workplane("XY")
      .polyline(pts)
      .close()
      .extrude(th)
)

# Cut the slot at the butt end
slot_w = 0.5
result = (
    result
      .faces(">Z")
      .workplane()
      .center(L1/2, 0)
      .rect(L1, slot_w)
      .cutThruAll()
)