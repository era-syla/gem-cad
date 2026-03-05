import cadquery as cq

path = cq.Workplane("XY").spline([(0, 0), (1, 2), (3, 4)], tangents=((0, 1), (1, 0)))

result = cq.Workplane("XY").circle(1).sweep(path)