import cadquery as cq
import math

R = 50
thickness = 5
rPath = 40
slotWidth = 4
angle1 = 20
angle2 = 80

a1 = math.radians(angle1)
a2 = math.radians(angle2)
am = math.radians((angle1 + angle2) / 2)

ro = rPath + slotWidth / 2
ri = rPath - slotWidth / 2

p1o = (ro * math.cos(a1), ro * math.sin(a1))
p2o = (ro * math.cos(a2), ro * math.sin(a2))
pm_o = (ro * math.cos(am), ro * math.sin(am))

p2i = (ri * math.cos(a2), ri * math.sin(a2))
p1i = (ri * math.cos(a1), ri * math.sin(a1))
pm_i = (ri * math.cos(am), ri * math.sin(am))

# Create the quarter‐circle wedge
result = (
    cq.Workplane("XY")
    .moveTo(R, 0)
    .threePointArc((0, R), (R / math.sqrt(2), R / math.sqrt(2)))
    .lineTo(0, 0)
    .close()
    .extrude(thickness)
)

# Cut the curved slot
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(*p1o)
    .threePointArc(p2o, pm_o)
    .lineTo(*p2i)
    .threePointArc(p1i, pm_i)
    .close()
    .cutBlind(-thickness)
)

# Cut the circular hole
hole_center = (30 * math.cos(am), 30 * math.sin(am))
result = (
    result
    .faces(">Z")
    .workplane()
    .center(*hole_center)
    .circle(3)
    .cutBlind(-thickness)
)