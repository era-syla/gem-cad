import cadquery as cq

thickness = 8
outer_dia = 60
fillet_r = 5
small_hole_d = 6
large_hole_d = 12

# Coordinates of the triangle vertices for a regular triangle of circumscribed diameter = outer_dia
R = outer_dia/2
import math
verts = [
    (R*math.cos(math.radians(0)),   R*math.sin(math.radians(0))),
    (R*math.cos(math.radians(120)), R*math.sin(math.radians(120))),
    (R*math.cos(math.radians(240)), R*math.sin(math.radians(240))),
]

# Build the bracket
result = (
    cq.Workplane("XY")
    .polygon(3, outer_dia)
    .extrude(thickness)
    .edges("|Z").fillet(fillet_r)
    .faces(">Z").workplane()
    # two small holes at the first two vertices
    .pushPoints([verts[0], verts[1]]).hole(small_hole_d)
    # one larger hole at the third vertex
    .pushPoints([verts[2]]).hole(large_hole_d)
)