import cadquery as cq

# Create outer and inner boxes for shell
outer = cq.Workplane("XY").box(100, 40, 40)
inner = cq.Workplane("XY").transformed(offset=(0, 0, 1)).box(96, 36, 38)
part = outer.cut(inner)

# Front face circle cut
part = part.faces("<X").workplane().pushPoints([(-10, -7)]).circle(6).cutThruAll()

# Front face rectangular cut
part = part.faces("<X").workplane().pushPoints([(10, -7)]).rect(30, 12).cutThruAll()

# Side vents
vent_points = [(-30, 0), (-15, 0), (0, 0), (15, 0), (30, 0)]
part = part.faces(">Y").workplane().pushPoints(vent_points).rect(3, 20).cutThruAll()

result = part