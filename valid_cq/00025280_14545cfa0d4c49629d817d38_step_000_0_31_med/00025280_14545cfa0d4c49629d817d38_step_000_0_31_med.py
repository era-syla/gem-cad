import cadquery as cq

# Parameters for the parametric model
D = 20.0            # Width and height of the main body
L = 40.0            # Length of the straight central section
hole_dia = 8.0      # Diameter of the holes
slot_width = 8.0    # Width of the cut slots
slot_depth = 16.0   # Depth of the slots from the tips

# 1. Create the base solid parts
# Central rectangular body
body = cq.Workplane("XY").box(L, D, D)

# Front rounded end (cylinder along Z-axis)
front_end = cq.Workplane("XY").transformed(offset=(-L/2, 0, 0)).cylinder(D, D/2)

# Back rounded end (cylinder along Y-axis, so we use XZ plane)
back_end = cq.Workplane("XZ").transformed(offset=(L/2, 0, 0)).cylinder(D, D/2)

# Combine into a single blank body
result = body.union(front_end).union(back_end)

# 2. Perform the slot cuts
# Front slot (Horizontal cut) - centered at the front tip
front_slot = cq.Workplane("XY").transformed(offset=(-L/2 - D/2, 0, 0)).box(slot_depth * 2, D + 5, slot_width)
result = result.cut(front_slot)

# Back slot (Vertical cut) - centered at the back tip
back_slot = cq.Workplane("XY").transformed(offset=(L/2 + D/2, 0, 0)).box(slot_depth * 2, slot_width, D + 5)
result = result.cut(back_slot)

# 3. Perform the hole cuts
# Front hole (Vertical)
front_hole = cq.Workplane("XY").transformed(offset=(-L/2, 0, 0)).cylinder(D + 5, hole_dia/2)
result = result.cut(front_hole)

# Back hole (Horizontal)
back_hole = cq.Workplane("XZ").transformed(offset=(L/2, 0, 0)).cylinder(D + 5, hole_dia/2)
result = result.cut(back_hole)