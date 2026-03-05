import cadquery as cq

# Parameters
L = 60          # total length in X
W = 15          # total width in Y
H = 10          # total height in Z
chamfer_dist = 2
slot_depth = 15
slot_width = 6
slot_height = 3

# Build the main block, front chamfer, and rear slot
result = (
    cq.Workplane("XY")
    .box(L, W, H, centered=(True, True, False))
    .faces(">X")
    .edges("|Z")
    .chamfer(chamfer_dist)
    .faces(">Z")
    .workplane()
    .center(-L/2 + slot_depth/2, 0)
    .rect(slot_depth, slot_width)
    .cutBlind(slot_height)
)