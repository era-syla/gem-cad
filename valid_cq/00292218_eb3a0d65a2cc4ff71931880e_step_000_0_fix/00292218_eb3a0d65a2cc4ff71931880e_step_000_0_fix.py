import cadquery as cq

thickness = 5
outerR = 20
innerR = 12
lugR = 8
holeR = 3
offset = 40
armWidth = 10
rectLength = offset - outerR
yOffset = 15

# Central ring
ring = cq.Workplane("XY")\
    .circle(outerR)\
    .circle(innerR)\
    .extrude(thickness)

# Left arm rectangle
rec1 = cq.Workplane("XY")\
    .rect(rectLength, armWidth)\
    .translate((-(outerR + rectLength/2), -yOffset, 0))\
    .extrude(thickness)

# Right arm rectangle
rec2 = cq.Workplane("XY")\
    .rect(rectLength, armWidth)\
    .translate((outerR + rectLength/2, yOffset, 0))\
    .extrude(thickness)

# Left lug
lug1 = cq.Workplane("XY")\
    .circle(lugR)\
    .translate((-offset, -yOffset, 0))\
    .extrude(thickness)

# Right lug
lug2 = cq.Workplane("XY")\
    .circle(lugR)\
    .translate((offset, yOffset, 0))\
    .extrude(thickness)

# Combine all solids
body = ring.union(rec1).union(rec2).union(lug1).union(lug2)

# Drill through holes in lugs
result = body.faces(">Z")\
    .workplane()\
    .pushPoints([(-offset, -yOffset), (offset, yOffset)])\
    .hole(2 * holeR)