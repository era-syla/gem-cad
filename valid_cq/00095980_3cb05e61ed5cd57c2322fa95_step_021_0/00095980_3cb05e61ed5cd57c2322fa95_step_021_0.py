import cadquery as cq

# Parameters for the extrusion (metric 2020 profile)
length = 500.0         # Length of the extrusion
width = 20.0           # Width/Height of the profile
corner_radius = 1.5    # Radius of the outer corners
center_hole_dia = 5.0  # Diameter of the central hole

# Slot dimensions (approximate for standard T-slot)
slot_opening_w = 6.2   # Width of the slot opening
slot_opening_d = 1.8   # Depth of the slot opening (neck)
slot_inner_w = 9.0     # Width of the inner cavity
slot_inner_d = 4.5     # Depth of the inner cavity (below the neck)

# 1. Create the base solid bar with rounded corners
result = (
    cq.Workplane("XY")
    .box(width, width, length)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Define the geometry for the T-slot cutter (on one side)
# We create a cutter aligned with the +Y face, then rotate it for other faces.
# Neck part of the slot
c_neck = (
    cq.Workplane("XY")
    .center(0, width/2 - slot_opening_d/2)
    .box(slot_opening_w, slot_opening_d, length)
)
# Inner cavity part of the slot
c_inner = (
    cq.Workplane("XY")
    .center(0, width/2 - slot_opening_d - slot_inner_d/2)
    .box(slot_inner_w, slot_inner_d, length)
)
# Combine to form the T-shape cutter
cutter = c_neck.union(c_inner)

# 3. Cut the slots on all 4 faces
for i in range(4):
    angle = i * 90
    # Rotate the cutter around the Z axis to align with each face
    rotated_cutter = cutter.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(rotated_cutter)

# 4. Create the central hole running through the length
result = (
    result.faces(">Z")
    .workplane()
    .hole(center_hole_dia)
)