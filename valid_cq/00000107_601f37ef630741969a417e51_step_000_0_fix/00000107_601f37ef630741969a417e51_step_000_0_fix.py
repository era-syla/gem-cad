import cadquery as cq

# Parameters
thickness = 5.0
length_horiz = 60.0
length_vert = 40.0
width = 20.0
slot_w = 4.0
slot_l = 20.0

# Top L‐shaped bracket
points = [
    (0, 0),
    (length_horiz, 0),
    (length_horiz, width),
    (length_vert, width),
    (length_vert, width + length_vert),
    (0, width + length_vert),
]
shape1 = cq.Workplane("XY").polyline(points).close().extrude(thickness)

# Cut a rectangular slot in the horizontal arm
slot1 = (
    cq.Workplane("XY")
    .box(slot_l, slot_w, thickness + 1)
    .translate((length_horiz / 2, width / 2, thickness / 2))
)
# Cut a rectangular slot in the vertical arm
slot2 = (
    cq.Workplane("XY")
    .box(slot_w, slot_l, thickness + 1)
    .translate((length_vert / 2, width + length_vert / 2, thickness / 2))
)

shape1 = shape1.cut(slot1).cut(slot2)

# Bottom sloped bar
wedge_length = 80.0
wedge_width = 10.0
slope = 3.0

points2 = [
    (0, 0),
    (wedge_length, slope),
    (wedge_length, wedge_width - slope),
    (0, wedge_width),
]
shape2 = cq.Workplane("XY").polyline(points2).close().extrude(thickness)
shape2 = shape2.rotate((0, 0, 0), (0, 0, 1), -15).translate((-10, -30, 0))

# Combine both parts
result = shape1.union(shape2)