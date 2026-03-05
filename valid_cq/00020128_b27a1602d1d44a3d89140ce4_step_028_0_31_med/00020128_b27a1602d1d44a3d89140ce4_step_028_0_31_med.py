import cadquery as cq

# Parametric dimensions
r_out = 20
r_in = 18
h_total = 100
h_flange = 25
w_window = 24
h_window_bottom = h_flange + 4
bridge_width = 12

# 1. Base Solid Cylinder
result = cq.Workplane("XY").circle(r_out).extrude(h_total)

# 2. Add Middle and Bottom Flanges
mid_flange = cq.Workplane("XY").workplane(offset=h_flange).circle(r_out + 3).extrude(2)
bot_flange = cq.Workplane("XY").circle(r_out + 4).extrude(2)
result = result.union(mid_flange).union(bot_flange)

# 3. Add Bottom Teeth (Polar Array)
teeth = cq.Workplane("XY").polarArray(r_out + 2, 0, 360, 24).rect(3, 5).extrude(2)
result = result.union(teeth)

# 4. Hollow out the interior bore
core_cutter = cq.Workplane("XY").circle(r_in).extrude(h_total)
result = result.cut(core_cutter)

# 5. Front Window Cut (with filleted bottom corners)
w2 = w_window / 2
z_bot = h_window_bottom
z_top = h_total + 10
rad = 4

window_cutter = (
    cq.Workplane("XZ")
    .workplane(offset=r_out + 10)
    .moveTo(0, z_bot)
    .lineTo(w2 - rad, z_bot)
    .radiusArc((w2, z_bot + rad), rad)
    .lineTo(w2, z_top)
    .lineTo(-w2, z_top)
    .lineTo(-w2, z_bot + rad)
    .radiusArc((-w2 + rad, z_bot), rad)
    .close()
    .extrude(-(r_out + 10))
)
result = result.cut(window_cutter)

# 6. Bottom Notches
notch_cutter = cq.Workplane("XY").rect(16, r_out * 3).extrude(12)
result = result.cut(notch_cutter)

# 7. Top Bridge
bridge = (
    cq.Workplane("XY")
    .workplane(offset=h_total - 3)
    .rect(r_out * 2.5, bridge_width)
    .extrude(3)
)
# Trim the bridge to the outer radius of the cylinder
cylinder_core = cq.Workplane("XY").circle(r_out).extrude(h_total)
bridge = bridge.intersect(cylinder_core)
result = result.union(bridge)

# 8. Top Tabs (Outer wedges)
tab1 = (
    cq.Workplane("XZ")
    .workplane(offset=-bridge_width / 2)
    .center(r_out, h_total)
    .polyline([(0, 0), (5, 0), (0, -8)]).close()
    .extrude(bridge_width)
)

tab2 = (
    cq.Workplane("XZ")
    .workplane(offset=-bridge_width / 2)
    .center(-r_out, h_total)
    .polyline([(0, 0), (-5, 0), (0, -8)]).close()
    .extrude(bridge_width)
)

result = result.union(tab1).union(tab2)