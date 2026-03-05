import cadquery as cq

L = 120
r = 8
block_h = 4
block_th = 4
lug_width = 16
d_hole = 4
slot_width = 4
slot_length = L - 20

result = cq.Workplane("XY").cylinder(L, radius=r)

# cut through slot on one side
result = result.cut(
    cq.Workplane("XY")
      .workplane(offset=r)
      .rect(slot_length, slot_width)
      .extrude(-2 * r)
)

# add lugs with holes at both ends
for x_pos in (L/2, -L/2):
    for signZ in (1, -1):
        lug = (
            cq.Workplane("YZ")
              .workplane(offset=x_pos)
              .center(0, signZ * (r + block_h/2))
              .rect(lug_width, block_h)
              .extrude(-block_th)
              .faces(">X")
              .workplane()
              .hole(d_hole)
        )
        result = result.union(lug)