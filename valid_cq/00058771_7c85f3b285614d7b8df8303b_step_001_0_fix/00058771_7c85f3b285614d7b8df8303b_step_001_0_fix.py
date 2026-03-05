import cadquery as cq

# Parameters
length = 100.0
profile_size = 20.0
slot_width = 6.0
slot_depth = 5.0
hole_dia = 5.0

# Create outer profile
base = cq.Workplane("XY").rect(profile_size, profile_size).extrude(length)

# Prepare cut shapes
half = profile_size / 2.0

# Slot on +X face
slot1 = cq.Workplane("XY").transformed(offset=(half + slot_depth/2, 0, 0)).box(
    slot_depth, slot_width, length
)

# Slot on -X face
slot2 = cq.Workplane("XY").transformed(offset=(-(half + slot_depth/2), 0, 0)).box(
    slot_depth, slot_width, length
)

# Slot on +Y face
slot3 = cq.Workplane("XY").transformed(offset=(0, half + slot_depth/2, 0)).box(
    slot_width, slot_depth, length
)

# Slot on -Y face
slot4 = cq.Workplane("XY").transformed(offset=(0, -(half + slot_depth/2), 0)).box(
    slot_width, slot_depth, length
)

# Central through hole
hole = cq.Workplane("XY").circle(hole_dia / 2).extrude(length)

# Combine cuts
result = base.cut(slot1).cut(slot2).cut(slot3).cut(slot4).cut(hole)