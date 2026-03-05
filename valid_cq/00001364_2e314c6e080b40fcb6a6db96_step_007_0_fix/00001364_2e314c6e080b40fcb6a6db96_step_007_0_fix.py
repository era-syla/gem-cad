import cadquery as cq
import math

rail_length = 120
rail_w = 20
rail_h = 20
rail = cq.Workplane("XY").box(rail_length, rail_w, rail_h)

d = 30
angle = math.radians(60)
v1 = ( d,  0)
v2 = ( d*math.cos(angle),  d*math.sin(angle))
v3 = ( d*math.cos(angle), -d*math.sin(angle))
plate_thickness = 5
hole_dia = 5

plate = (
    cq.Workplane("XY")
    .polyline([v1, v2, v3])
    .close()
    .extrude(plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([v1, v2, v3])
    .hole(hole_dia)
    .translate((0, 0, -plate_thickness/2))
)

rail1 = rail
rail2 = rail.rotate((0, 0, 0), (0, 0, 1), 60)
rail3 = rail.rotate((0, 0, 0), (0, 0, 1), -60)

result = rail1.union(rail2).union(rail3).union(plate)