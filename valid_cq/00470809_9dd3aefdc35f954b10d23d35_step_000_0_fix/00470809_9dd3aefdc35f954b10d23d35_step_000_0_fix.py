import cadquery as cq

# Parameters
length = 200
width = 30
height = 10
rail_thickness = 2
slot_depth = 6
slot_height = height - 2 * rail_thickness

# Create the main extrusion
base = cq.Workplane("XY").box(width, length, height)

# Create side slot on +X side
slot1 = (
    cq.Workplane("XY")
    .transformed(offset=(width/2 - slot_depth/2, 0, 0))
    .box(slot_depth, length, slot_height)
)

# Create side slot on -X side
slot2 = (
    cq.Workplane("XY")
    .transformed(offset=(-width/2 + slot_depth/2, 0, 0))
    .box(slot_depth, length, slot_height)
)

# Cut the slots out of the base
result = base.cut(slot1).cut(slot2)