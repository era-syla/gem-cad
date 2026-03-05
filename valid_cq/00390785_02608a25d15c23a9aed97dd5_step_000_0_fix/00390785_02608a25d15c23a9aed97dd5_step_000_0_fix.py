import cadquery as cq

big_sphere = cq.Workplane("XY").sphere(20)
small_sphere = cq.Workplane("XY").sphere(10).translate((0, 0, 30))

result = big_sphere.union(small_sphere)