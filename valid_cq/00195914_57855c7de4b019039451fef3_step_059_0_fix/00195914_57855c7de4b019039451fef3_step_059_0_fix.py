import cadquery as cq

# Parameters
outer = 20
slot_width = 6
slot_depth = 8
length = 200

# Base extrusion
base = cq.Workplane("XY").rect(outer, outer).extrude(length)

# Create slot-cutting boxes
cuts = []
# +X slot
cuts.append(
    cq.Workplane("XY")
    .box(slot_depth, slot_width, length)
    .translate((outer/2 - slot_depth/2, 0, length/2))
)
# -X slot
cuts.append(
    cq.Workplane("XY")
    .box(slot_depth, slot_width, length)
    .translate((-outer/2 + slot_depth/2, 0, length/2))
)
# +Y slot
cuts.append(
    cq.Workplane("XY")
    .box(slot_width, slot_depth, length)
    .translate((0, outer/2 - slot_depth/2, length/2))
)
# -Y slot
cuts.append(
    cq.Workplane("XY")
    .box(slot_width, slot_depth, length)
    .translate((0, -outer/2 + slot_depth/2, length/2))
)

# Subtract slots from base
result = base
for cut in cuts:
    result = result.cut(cut)