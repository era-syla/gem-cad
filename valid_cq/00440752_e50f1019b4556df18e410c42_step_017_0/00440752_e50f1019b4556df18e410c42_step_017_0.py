import cadquery as cq

# Key dimensions based on the visual proportions
length = 90.0
width = 45.0
thickness = 10.0
slot_width = 4.0
slot_depth = 4.0

# The slots divide the length into three roughly equal sections
# Center-to-center distance between the two slots
slot_separation = length / 3.0

result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    # Position the slots symmetrically around the center
    .pushPoints([(-slot_separation / 2.0, 0), (slot_separation / 2.0, 0)])
    .rect(slot_width, width)
    .cutBlind(-slot_depth)
)