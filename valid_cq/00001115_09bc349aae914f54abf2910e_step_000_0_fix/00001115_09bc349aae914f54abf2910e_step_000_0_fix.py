import cadquery as cq

th = 3.0
w1 = 10.0
z1 = 40.0
w2 = 30.0
z2 = 60.0
z3 = 80.0
fl_top = 20.0
fl_bot = 10.0

# Central upright profile in the XZ plane, extruded in Y for thickness
pts = [(-w1, 0), (-w1, z1), (-w2, z2), (-w2, z3), (w2, z3), (w2, z2), (w1, z1), (w1, 0)]
central = cq.Workplane("XZ").polyline(pts).close().extrude(th)

# Top flange profile
top_flange = (
    cq.Workplane("XZ")
    .polyline([(-w2, z3), (w2, z3), (w2, z3 + fl_top), (-w2, z3 + fl_top)])
    .close()
    .extrude(th)
)

# Bottom flange profile
bot_flange = (
    cq.Workplane("XZ")
    .polyline([(-w1, 0), (w1, 0), (w1, -fl_bot), (-w1, -fl_bot)])
    .close()
    .extrude(th)
)

# Combine bodies
result = central.union(top_flange).union(bot_flange)

# Add holes and slot on the face of thickness (+Y)
# Large center hole
z_c = (z2 + z3) / 2
result = result.faces(">Y").workplane().center(0, z_c).hole(12)

# Wing holes
x_h = w2 - 10.0
z_h = z2 - 5.0
result = (
    result.faces(">Y")
    .workplane()
    .center(-x_h, z_h)
    .hole(4)
    .center(2 * x_h, 0)
    .hole(4)
)

# Bottom flange hole
result = result.faces(">Y").workplane().center(0, -fl_bot / 2).hole(4)

# Top slot
slot_len = 12.0
slot_w = 5.0
result = (
    result.faces(">Y")
    .workplane()
    .center(0, z3 + fl_top / 2)
    .rect(slot_len, slot_w)
    .extrude(-th)
)