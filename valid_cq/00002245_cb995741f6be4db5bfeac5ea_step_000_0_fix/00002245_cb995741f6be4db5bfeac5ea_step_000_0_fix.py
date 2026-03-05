import cadquery as cq

# Parameters
L, W, H = 60, 60, 60  # box dimensions: length (X), width (Y), height (Z)
r = 3                 # edge fillet radius
hole_d = 20           # diameter of circular hole
hole_off_x, hole_off_y = 10, 15  # hole offset from face center
slot_w, slot_h = 15, 8           # slot width and height
slot_off_x, slot_off_y = 15, -20 # slot offset from face center

# Create base box
result = cq.Workplane("XY").box(L, W, H)

# Fillet all edges
result = result.edges().fillet(r)

# Cut circular hole on the front (+X) face
result = (
    result
    .faces(">X")
    .workplane()
    .center(hole_off_x, hole_off_y)
    .hole(hole_d)
)

# Cut rectangular slot on the front (+X) face
result = (
    result
    .faces(">X")
    .workplane()
    .center(slot_off_x, slot_off_y)
    .rect(slot_w, slot_h)
    .cutThruAll()
)