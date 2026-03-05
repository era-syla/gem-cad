import cadquery as cq

profile = cq.Workplane("XY").spline(
    [(0, 0), (5, 0), (7.5, 30), (2, 50), (2, 60), (5, 70)]
).close()

result = profile.revolve()