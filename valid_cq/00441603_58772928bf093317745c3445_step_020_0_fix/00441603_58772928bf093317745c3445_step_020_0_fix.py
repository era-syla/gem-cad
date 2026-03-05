import cadquery as cq

length = 100.0
radius = 10.0
slot_width = 4.0
slot_depth = 8.0
end_clearance = 10.0
slot_length = length - 2 * end_clearance

cylinder = cq.Workplane("XY").circle(radius).extrude(length)
slot_cut = (
    cq.Workplane("XY", origin=(0, radius - slot_depth, end_clearance + slot_length / 2))
    .box(slot_width, slot_depth, slot_length, centered=(True, False, True))
)
result = cylinder.cut(slot_cut)