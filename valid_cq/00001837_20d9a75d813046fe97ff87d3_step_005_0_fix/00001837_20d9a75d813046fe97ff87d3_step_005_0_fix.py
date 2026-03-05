import cadquery as cq

r = 2
points = [(0, 0), (80, 0), (100, 20), (180, 20), (200, 0)]
path_wire = cq.Workplane("XZ").spline(points).val()

result = cq.Workplane("YZ").circle(r).sweep(path_wire)