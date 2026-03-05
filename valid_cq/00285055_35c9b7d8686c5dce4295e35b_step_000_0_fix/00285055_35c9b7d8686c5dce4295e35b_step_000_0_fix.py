import cadquery as cq

R_big = 15
R_small = 5
L = 80
thickness = 10
bar_height = 10
hole_big = 5
hole_small = 3
slot_length = L - 2*R_small - 20
slot_radius = 2

# Create big and small cylinders
big_cyl = cq.Workplane("XY").circle(R_big).extrude(thickness)
small_cyl = cq.Workplane("XY").transformed(offset=(L, 0, 0)).circle(R_small).extrude(thickness)

# Create connecting bar
bar = (
    cq.Workplane("XY")
    .transformed(offset=(R_small, -bar_height/2, 0))
    .rect(L - 2*R_small, bar_height)
    .extrude(thickness)
)

# Combine into one body
body = big_cyl.union(small_cyl).union(bar)

# Cut holes and slot
result = (
    body
    .faces(">Z")
    .workplane()
    .center(0, 0).circle(hole_big).cutThruAll()
    .faces(">Z")
    .workplane()
    .center(L, 0).circle(hole_small).cutThruAll()
    .faces(">Z")
    .workplane()
    .center(L/2, 0).slot2D(slot_length, slot_radius).cutThruAll()
)