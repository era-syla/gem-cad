import cadquery as cq
import math

# Base plate (vertical)
plate = cq.Workplane("XZ").rect(80, 60).extrude(8)
plate = plate.edges("|Y").fillet(4)
plate = plate.faces(">Y").workplane().circle(15).extrude(8)

# First link
L1 = 100
W1 = 12
T = 8
link1 = (
    cq.Workplane("XZ")
    .polyline([(0, -W1/2), (L1, -W1/2), (L1, W1/2), (0, W1/2)])
    .close()
    .extrude(T)
    .faces(">Y")
    .workplane()
    .pushPoints([(0, 0), (L1, 0)])
    .hole(8)
)
link1 = link1.rotate((0, 0, 0), (0, 1, 0), -45)

# Second link
L2 = 90
W2 = 12
link2 = (
    cq.Workplane("XZ")
    .polyline([(0, -W2/2), (L2, -W2/2), (L2, W2/2), (0, W2/2)])
    .close()
    .extrude(T)
    .faces(">Y")
    .workplane()
    .pushPoints([(0, 0), (L2, 0)])
    .hole(8)
)
link2 = link2.rotate((0, 0, 0), (0, 1, 0), 30)
fx = L1 * math.cos(math.radians(45))
fz = -L1 * math.sin(math.radians(45))
link2 = link2.translate((fx, 0, fz))

# Combine all parts
result = plate.union(link1).union(link2)