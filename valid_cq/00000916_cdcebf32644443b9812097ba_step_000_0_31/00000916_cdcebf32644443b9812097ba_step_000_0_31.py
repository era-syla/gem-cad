import cadquery as cq
import math

def gear_profile(radius, teeth, depth):
    pts = []
    for i in range(teeth * 2):
        angle = math.pi * 2 * i / (teeth * 2)
        r = radius if i % 2 == 0 else radius - depth
        pts.append((r * math.cos(angle), r * math.sin(angle)))
    return pts

# --- Main Body ---
b1 = cq.Workplane("XY").center(0, -2).box(18, 16, 16)
b1 = b1.edges("|Z").chamfer(1)

b2 = cq.Workplane("XY").center(0, 9).box(14, 6, 14)
b2 = b2.edges("|Z").chamfer(1)

body = b1.union(b2)

# --- Vertical Bore ---
top_boss = cq.Workplane("XY").workplane(offset=8).circle(7).extrude(3)
top_lip = cq.Workplane("XY").workplane(offset=11).circle(7.5).extrude(1.5)
body = body.union(top_boss).union(top_lip)

bottom_boss = cq.Workplane("XY").workplane(offset=-13).circle(5.5).extrude(5)
body = body.union(bottom_boss)

# Funnel shaped inner cut — use simple cylinders instead of revolve profile
body = body.cut(cq.Workplane("XY").workplane(offset=-14).circle(4.5).extrude(20))
body = body.cut(cq.Workplane("XY").workplane(offset=6).circle(4.5).extrude(7))
body = body.cut(cq.Workplane("XY").workplane(offset=11).circle(6.5).extrude(2))

# --- Throttle Assembly (-X Side) ---
t_shaft = cq.Workplane("YZ").workplane(offset=-8).circle(1.8).extrude(-12)
t_boss = cq.Workplane("YZ").workplane(offset=-9).circle(4).extrude(-1.5)

# Throttle Arm
arm_pts = [(-11.5, 4), (-12.5, 4), (-12.5, -4), (-15.5, -9), (-15.5, -14), (-13.5, -14), (-13.5, -10), (-11.5, -5)]
t_arm = cq.Workplane("XZ").polyline(arm_pts).close().extrude(4).translate((0, -2, 0))
t_arm = t_arm.cut(cq.Workplane("YZ").workplane(offset=-10).circle(2.0).extrude(-10))
t_arm = t_arm.cut(cq.Workplane("YZ").workplane(offset=-10).center(0, -12).circle(0.8).extrude(-10))
try:
    t_arm = t_arm.edges("|Y").fillet(0.5)
except:
    pass

t_washer = cq.Workplane("YZ").workplane(offset=-13.5).circle(3.5).extrude(-0.5)
t_nut = cq.Workplane("YZ").workplane(offset=-14).polygon(6, 6).extrude(-3)

throttle_assm = t_shaft.union(t_boss).union(t_arm).union(t_washer).union(t_nut)

# Shaft end slot
t_slot_cut = cq.Workplane("YZ").workplane(offset=-20).rect(4, 0.8).extrude(1.5)
throttle_assm = throttle_assm.cut(t_slot_cut)

body = body.union(throttle_assm)

# --- Needle Valve Assembly (+Y Side) ---
n_boss = cq.Workplane("XZ").workplane(offset=12).circle(5).extrude(2)

# Large Knurled Nut
pts_nut = gear_profile(6, 30, 0.4)
n_nut = cq.Workplane("XZ").workplane(offset=14).polyline(pts_nut).close().extrude(3)

# Threaded Shaft
n_shaft = cq.Workplane("XZ").workplane(offset=17).circle(2).extrude(8)
needle_assm = n_boss.union(n_nut).union(n_shaft)

for i in range(7):
    n_ring = cq.Workplane("XZ").workplane(offset=17.5 + i).circle(2.4).extrude(0.5)
    needle_assm = needle_assm.union(n_ring)

# Small Knurled Knob
pts_knob = gear_profile(5, 24, 0.4)
n_knob = cq.Workplane("XZ").workplane(offset=25).polyline(pts_knob).close().extrude(4)
needle_assm = needle_assm.union(n_knob)

# Tip
n_tip = cq.Workplane("XZ").workplane(offset=29).circle(1.5).extrude(3)
needle_assm = needle_assm.union(n_tip)

body = body.union(needle_assm)

# --- Idle Adjustment Screw (Top Face) ---
i_boss = cq.Workplane("XY").workplane(offset=8).center(-5, -5).circle(2.5).extrude(1.5)
i_head = cq.Workplane("XY").workplane(offset=9.5).center(-5, -5).circle(2.2).extrude(1.5)
idle_assm = i_boss.union(i_head)

# Screw slot
i_slot = cq.Workplane("XY").workplane(offset=11).center(-5, -5).rect(5, 0.8).extrude(-1)
idle_assm = idle_assm.cut(i_slot)

body = body.union(idle_assm)

result = body