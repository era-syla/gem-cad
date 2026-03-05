import cadquery as cq

thickness = 5
hbar_len = 100
hbar_width = 10
slot_length = 60
slot_width = 4
big_hole_d = 8
small_hole_d = 4
vbar_width = 6
vbar_height = 50
end_margin = 5
small_hole_offset = 20

# Top horizontal bar
top_bar = (
    cq.Workplane("XY")
    .transformed(offset=(0, vbar_height/2, 0))
    .rect(hbar_len, hbar_width)
    .extrude(thickness)
    .faces(">Z").workplane()
    .pushPoints([(-small_hole_offset, 0), (small_hole_offset, 0)])
    .hole(small_hole_d)
    .pushPoints([(-hbar_len/2 + end_margin, 0), (hbar_len/2 - end_margin, 0)])
    .hole(big_hole_d)
    .rect(slot_length, slot_width)
    .cutThruAll()
)

# Bottom horizontal bar
bottom_bar = (
    cq.Workplane("XY")
    .transformed(offset=(0, -vbar_height/2, 0))
    .rect(hbar_len, hbar_width)
    .extrude(thickness)
    .faces(">Z").workplane()
    .pushPoints([(-small_hole_offset, 0), (small_hole_offset, 0)])
    .hole(small_hole_d)
    .pushPoints([(-hbar_len/2 + end_margin, 0), (hbar_len/2 - end_margin, 0)])
    .hole(big_hole_d)
    .rect(slot_length, slot_width)
    .cutThruAll()
)

# Vertical connecting bar
vbar = (
    cq.Workplane("XY")
    .rect(vbar_width, vbar_height)
    .extrude(thickness)
)

result = top_bar.union(bottom_bar).union(vbar)