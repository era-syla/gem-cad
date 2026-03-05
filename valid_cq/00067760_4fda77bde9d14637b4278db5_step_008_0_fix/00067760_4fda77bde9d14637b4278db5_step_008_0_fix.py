import cadquery as cq

# Parameters
bigR = 20.0
centerDistance = 50.0
flangeHeight = 10.0
thickness = 5.0
bigHoleDiam = 30.0
smallHoleDiam = 6.0

# Derived
rectWidth = 2*bigR + centerDistance
rectHeight = flangeHeight
rectCenterY = -bigR - rectHeight/2

# Build main body by extruding two circles and a bottom rectangle, then fusing
c1 = cq.Workplane("XY").center(-centerDistance/2, 0).circle(bigR).extrude(thickness)
c2 = cq.Workplane("XY").center( centerDistance/2, 0).circle(bigR).extrude(thickness)
rect = cq.Workplane("XY").center(0, rectCenterY).rect(rectWidth, rectHeight).extrude(thickness)
result = c1.union(c2).union(rect)

# Cut out the two large holes
result = result.faces(">Z").workplane().pushPoints([
    (-centerDistance/2, 0),
    ( centerDistance/2, 0),
]).hole(bigHoleDiam)

# Cut out the six smaller fastener holes
smallPts = [
    (-centerDistance/2,  bigR*0.6),
    ( centerDistance/2,  bigR*0.6),
    (-centerDistance/2, -bigR*0.6),
    ( centerDistance/2, -bigR*0.6),
    (0,                  bigR*0.8),
    (0,                 -bigR*0.8),
]
result = result.faces(">Z").workplane().pushPoints(smallPts).hole(smallHoleDiam)