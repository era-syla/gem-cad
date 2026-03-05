import cadquery as cq

thickness = 5
H = 50
arm_len = 80
hook_len = 10
drop = 10

points = [
    (0, 0),
    (0, H),
    (arm_len + hook_len, H),
    (arm_len + hook_len, H - drop),
    (arm_len, H - drop),
]

result = cq.Workplane("XZ").polyline(points).close().extrude(thickness)