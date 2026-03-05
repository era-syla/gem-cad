import cadquery as cq

thickness = 2.0
pts1 = [(0, 0), (-30, 10), (-30, -10)]
pts2 = [(0, 0), (30, 10), (30, -10)]

tri1 = cq.Workplane("XY").polyline(pts1).close().extrude(thickness)
tri2 = cq.Workplane("XY").polyline(pts2).close().extrude(thickness)

result = tri1.union(tri2)