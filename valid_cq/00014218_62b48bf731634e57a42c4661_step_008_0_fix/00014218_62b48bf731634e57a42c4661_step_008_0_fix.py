import cadquery as cq

wheel_r = 15
th = 4
wheel_dist = 60

w1 = cq.Workplane("XY").circle(wheel_r).extrude(th)
w2 = cq.Workplane("XY").transformed(offset=(wheel_dist, 0, 0)).circle(wheel_r).extrude(th)

frame_profile = [
    (15, 5),
    (15, 35),
    (45, 40),
    (55, 40),
    (55, 36),
    (47, 36),
    (47, 10),
    (15, 10)
]
frame = cq.Workplane("XY").polyline(frame_profile).close().extrude(th)

seat = cq.Workplane("XY").transformed(offset=(15, 35, th)).box(6, th, 3)

handlebar = (
    cq.Workplane("YZ")
    .transformed(offset=(45, 40, th))
    .circle(1)
    .extrude(30)
)

result = w1.union(w2).union(frame).union(seat).union(handlebar)