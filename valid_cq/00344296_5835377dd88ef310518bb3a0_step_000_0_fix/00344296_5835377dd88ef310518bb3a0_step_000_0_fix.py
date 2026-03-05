import cadquery as cq

thickness = 5.0

# Main profile of knife (handle + blade)
profile_pts = [
    (0, 0),
    (80, 0),
    (200, 5),
    (215, 20),
    (80, 20),
    (0, 20)
]

blade = (
    cq.Workplane("XY")
    .polyline(profile_pts)
    .close()
    .extrude(thickness)
)

# Finger guard notch
notch = (
    cq.Workplane("XY")
    .center(80, 5)
    .circle(6)
    .extrude(thickness)
)

result = blade.cut(notch)