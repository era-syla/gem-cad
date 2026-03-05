import cadquery as cq

# Base back plate
back_plate = cq.Workplane("XY").rect(40, 80).extrude(4)

# Front pocket
front_pocket = cq.Workplane("XY").rect(30, 50).extrude(6).translate((0, 15, 4))

# Bottom legs
leg1 = cq.Workplane("XY").rect(8, 20).extrude(4).translate((-12, -50, 0))
leg2 = cq.Workplane("XY").rect(8, 20).extrude(4).translate((12, -50, 0))

# Holes in legs
hole1 = cq.Workplane("XY").transformed(offset=(-12, -50, 0)).circle(3).extrude(4)
hole2 = cq.Workplane("XY").transformed(offset=(12, -50, 0)).circle(3).extrude(4)

# Top clamps
clamp_left = cq.Workplane("XY").rect(4, 20).extrude(6).translate((-8, 65, 4))
clamp_right = cq.Workplane("XY").rect(4, 20).extrude(6).translate((8, 65, 4))

# Ribs on front face
rib1 = cq.Workplane("XY").polyline([(-5, 25), (0, 40), (5, 25)]).close().extrude(4).translate((0, 0, 4))
rib2 = cq.Workplane("XY").polyline([(-5, 10), (0, 20), (5, 10)]).close().extrude(4).translate((0, 0, 4))
rib3 = cq.Workplane("XY").polyline([(-5, 35), (0, 45), (5, 35)]).close().extrude(4).translate((0, 0, 4))

# Assemble everything
result = (
    back_plate
    .union(front_pocket)
    .union(leg1)
    .union(leg2)
    .union(clamp_left)
    .union(clamp_right)
    .union(rib1)
    .union(rib2)
    .union(rib3)
    .cut(hole1)
    .cut(hole2)
)