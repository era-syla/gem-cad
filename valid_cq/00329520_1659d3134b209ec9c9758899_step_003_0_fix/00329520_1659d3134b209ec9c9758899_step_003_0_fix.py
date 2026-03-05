import cadquery as cq

L = 200
W = 10
H = 10
hole_d = 3
count = 8

# Compute hole positions along the X axis centered on the bar
points = [(L * (i / (count - 1) - 0.5), 0) for i in range(count)]

result = (
    cq.Workplane("XY")
    .box(L, W, H)
    .faces(">Z")
    .workplane()
    .pushPoints(points)
    .hole(hole_d)
)