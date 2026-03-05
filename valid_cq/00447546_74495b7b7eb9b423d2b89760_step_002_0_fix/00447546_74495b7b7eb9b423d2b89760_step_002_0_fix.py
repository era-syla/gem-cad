import cadquery as cq

L = 100
slot_width = 6
slot_depth = 7

# Create main extrusion, center it on the origin in Z
outer = cq.Workplane("XY").rect(20, 20).extrude(L).translate((0, 0, -L/2))

# Create cutting boxes for the four T‐slots
slot_x = cq.Workplane("XY").box(slot_depth, slot_width, L + 2)
slot_x_pos = slot_x.translate((10 - slot_depth/2, 0, 0))
slot_x_neg = slot_x.translate((-10 + slot_depth/2, 0, 0))

slot_y = cq.Workplane("XY").box(slot_width, slot_depth, L + 2)
slot_y_pos = slot_y.translate((0, 10 - slot_depth/2, 0))
slot_y_neg = slot_y.translate((0, -10 + slot_depth/2, 0))

# Subtract the slots from the main body
result = outer.cut(slot_x_pos).cut(slot_x_neg).cut(slot_y_pos).cut(slot_y_neg)

# Cut the central through‐hole along the length
result = result.workplane(origin=(0, 0, -L/2)).circle(5).cutThruAll()