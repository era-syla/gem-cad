import cadquery as cq

length = 200
cross = 5

result = cq.Workplane("XY").box(length, cross, cross)