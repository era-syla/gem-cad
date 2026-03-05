import cadquery as cq
import math

R_outer = 50
R_inner = 40
ring_thickness = 5
fin_height = 20
fin_thickness = 8
angles = [0, 120, 240]
radial_length = R_outer - R_inner

ring = cq.Workplane("XY").circle(R_outer).circle(R_inner).extrude(ring_thickness)

fins = []
for ang in angles:
    fin = (
        cq.Workplane("XY")
        .transformed(rotate=(0, 0, ang))
        .transformed(offset=((R_outer + R_inner) / 2, 0, ring_thickness))
        .rect(radial_length, fin_thickness)
        .extrude(fin_height)
    )
    fins.append(fin)

result = ring.union(*fins)