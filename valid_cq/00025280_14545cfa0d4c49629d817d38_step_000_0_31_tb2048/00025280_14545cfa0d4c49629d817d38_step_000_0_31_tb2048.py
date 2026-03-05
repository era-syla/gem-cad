import cadquery as cq

# Parametric dimensions
L = 45.0             # Center-to-center distance between holes
W = 20.0             # Width and height of the central block
R = W / 2.0          # Radius of the rounded ends
gap = 8.0            # Gap width of the slots
hole_dia = 8.0       # Diameter of the through holes
slot_overlap = 8.0   # How far the slot extends past the hole center into the body

# 1. Create the central body block
body = cq.Workplane("XY").box(L, W, W)

# 2. Add the rounded ends
# Left end is rounded around the Z-axis (vertical cylinder)
left_cyl = cq.Workplane("XY").center(-L/2, 0).cylinder(W, R)

# Right end is rounded around the Y-axis (horizontal cylinder)
# XZ plane has its normal along the Y-axis
right_cyl = cq.Workplane("XZ").center(L/2, 0).cylinder(W, R)

# Combine into a single solid base
base = body.union(left_cyl).union(right_cyl)

# 3. Create the cutting tools for the slots
slot_length = R + slot_overlap
left_slot_x = -L/2 - R + slot_length / 2.0
right_slot_x = L/2 + R - slot_length / 2.0

# Left slot is horizontal (cuts through Y, leaves prongs separated in Z)
left_slot = cq.Workplane("XY").center(left_slot_x, 0).box(slot_length, W + 5, gap)

# Right slot is vertical (cuts through Z, leaves prongs separated in Y)
right_slot = cq.Workplane("XY").center(right_slot_x, 0).box(slot_length, gap, W + 5)

# Apply the slot cuts
with_slots = base.cut(left_slot).cut(right_slot)

# 4. Create and cut the holes
# Left hole is vertical (along Z-axis)
left_hole = cq.Workplane("XY").center(-L/2, 0).cylinder(W + 5, hole_dia / 2.0)

# Right hole is horizontal (along Y-axis)
right_hole = cq.Workplane("XZ").center(L/2, 0).cylinder(W + 5, hole_dia / 2.0)

# Final resulting shape
result = with_slots.cut(left_hole).cut(right_hole)