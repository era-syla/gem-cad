import cadquery as cq

slot_width = 6
slot_depth = 8
size = 20
lengths = [200, 150, 100, 75, 50]
spacing = 30

beams = []
for i, L in enumerate(lengths):
    # outer beam
    outer = cq.Workplane("YZ").rect(size, size).extrude(L)
    # right slot block
    right_block = (
        cq.Workplane("XZ")
        .rect(L, slot_width)
        .extrude(slot_depth)
        .translate((0, size/2 - slot_depth/2, 0))
    )
    # left slot block
    left_block = (
        cq.Workplane("XZ")
        .rect(L, slot_width)
        .extrude(-slot_depth)
        .translate((0, -size/2 + slot_depth/2, 0))
    )
    # top slot block
    top_block = (
        cq.Workplane("XY")
        .rect(L, slot_width)
        .extrude(slot_depth)
        .translate((0, 0, size/2 - slot_depth/2))
    )
    # bottom slot block
    bottom_block = (
        cq.Workplane("XY")
        .rect(L, slot_width)
        .extrude(-slot_depth)
        .translate((0, 0, -size/2 + slot_depth/2))
    )
    beam = outer.cut(right_block).cut(left_block).cut(top_block).cut(bottom_block)
    beam = beam.translate((0, i * spacing, 0))
    beams.append(beam)

result = beams[0]
for b in beams[1:]:
    result = result.union(b)