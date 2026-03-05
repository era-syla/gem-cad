import cadquery as cq

w = 10
thk = 1
L_total = 100

# Define outline with a zigzag on the top edge between x=20 and x=40
pts = [
    (0, -w/2),
    (L_total, -w/2),
    (L_total,  w/2),
    (40,       w/2),
    (36,       w/2 - 4),
    (32,       w/2),
    (28,       w/2 - 4),
    (24,       w/2),
    (20,       w/2),
    (0,        w/2),
]

result = (
    cq.Workplane("XY")
      .polyline(pts)
      .close()
      .extrude(thk)
)

# Cut a keyhole at the left end: a circle of radius 4 at (10,0) and a 4×8 neck below it
result = (
    result
      .faces(">Z")
      .workplane()
      .moveTo(10, 0).circle(4)
      .moveTo(10, -8).rect(4, 8)
      .cutThruAll()
)