import cadquery as cq
import math

outer_d = 100
inner_d = 60
thickness = 5
hole_d = 10
bolt_circle_d = 80
n_holes = 8

result = (
    cq.Workplane("XY")
    .circle(outer_d/2)
    .circle(inner_d/2)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .polarArray(0, 0, bolt_circle_d/2, n_holes, 360)
    .hole(hole_d)
)