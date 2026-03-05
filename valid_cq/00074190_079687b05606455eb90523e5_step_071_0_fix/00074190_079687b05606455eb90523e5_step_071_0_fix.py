import cadquery as cq

R_center = 20
R_side = 12
spacing = 35
thickness = 8
hole_dia = 6

center = cq.Workplane("XY").circle(R_center).extrude(thickness)
side1 = cq.Workplane("XY", origin=( spacing, 0, 0)).circle(R_side).extrude(thickness)
side2 = cq.Workplane("XY", origin=(-spacing, 0, 0)).circle(R_side).extrude(thickness)

result = center.union(side1).union(side2) \
    .faces(">Z") \
    .workplane() \
    .center(0, 0) \
    .hole(hole_dia)