import cadquery as cq
import math

outer_d = 100
inner_d = 60
thickness = 10
hole_d = 5

# Radius at which holes are placed (midway in the ring)
hole_r = (outer_d/2 + inner_d/2) / 2

# Generate four hole positions equally spaced at 90°
points = [
    (hole_r * math.cos(math.radians(angle)), hole_r * math.sin(math.radians(angle)))
    for angle in (0, 90, 180, 270)
]

result = (
    cq.Workplane("XY")
    .circle(outer_d/2)
    .circle(inner_d/2)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(points)
    .hole(hole_d)
)