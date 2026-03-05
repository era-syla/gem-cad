import cadquery as cq
import math

# --- Parameters ---
# Frame Geometry (mm)
st_length = 540.0        # Seat Tube Length
st_angle = 73.0          # Seat Tube Angle
tt_length_eff = 550.0    # Effective Top Tube Length
ht_length = 150.0        # Head Tube Length
ht_angle = 73.0          # Head Tube Angle
cs_length = 410.0        # Chain Stay Length
rear_spacing = 130.0     # Rear Hub Width
bb_width = 68.0          # Bottom Bracket Width

# Tube Diameters (mm)
bb_od = 40.0
st_od = 28.6
tt_od = 31.8
dt_od = 34.9
ht_od = 40.0
cs_od = 19.0
ss_od = 16.0
dropout_od = 20.0

# --- Helper Function ---
def make_strut(p1, p2, diam):
    """Creates a cylinder strut between two points."""
    v = p2 - p1
    return cq.Solid.makeCylinder(diam / 2.0, v.Length, p1, v.normalized())

# --- Calculations & Points ---
# Origin is Center of Bottom Bracket (BB)
p_bb = cq.Vector(0, 0, 0)

# Seat Tube Vector & Top Point
st_rad = math.radians(st_angle)
st_vec = cq.Vector(-math.cos(st_rad), 0, math.sin(st_rad))
p_st_top = p_bb + st_vec * st_length

# Head Tube Placement
# Approximate HT position based on effective top tube (horizontal distance)
ht_rad = math.radians(ht_angle)
ht_vec = cq.Vector(-math.cos(ht_rad), 0, math.sin(ht_rad))

# Calculate center of HT relative to ST Top
ht_center_x = p_st_top.x + tt_length_eff
ht_center_z = p_st_top.z # Horizontal top tube assumption
p_ht_center = cq.Vector(ht_center_x, 0, ht_center_z)

# HT Start (Bottom) and End (Top)
p_ht_bot = p_ht_center - ht_vec * (ht_length * 0.6)
p_ht_top = p_ht_center + ht_vec * (ht_length * 0.4)

# Rear Dropouts
p_dropout_l = cq.Vector(-cs_length, rear_spacing / 2.0, 0)
p_dropout_r = cq.Vector(-cs_length, -rear_spacing / 2.0, 0)

# --- Geometry Construction ---

# 1. Bottom Bracket Shell
bb_shell = cq.Solid.makeCylinder(bb_od / 2.0, bb_width, cq.Vector(0, -bb_width / 2.0, 0), cq.Vector(0, 1, 0))

# 2. Seat Tube (with slight extension for clamp)
p_st_ext = p_st_top + st_vec * 20.0
seat_tube = make_strut(p_bb, p_st_ext, st_od)

# 3. Head Tube
head_tube = make_strut(p_ht_bot, p_ht_top, ht_od)

# 4. Top Tube
top_tube = make_strut(p_st_top, p_ht_center, tt_od)

# 5. Down Tube (Connects BB to lower part of HT)
p_dt_end = p_ht_bot + ht_vec * 20.0
down_tube = make_strut(p_bb, p_dt_end, dt_od)

# 6. Chain Stays
# Start offset from BB center to clear shell width
p_cs_start_l = cq.Vector(0, 15, 0)
p_cs_start_r = cq.Vector(0, -15, 0)
cs_l = make_strut(p_cs_start_l, p_dropout_l, cs_od)
cs_r = make_strut(p_cs_start_r, p_dropout_r, cs_od)

# 7. Seat Stays
# Start offset from ST Top
p_ss_start_l = p_st_top + cq.Vector(0, 18, -20)
p_ss_start_r = p_st_top + cq.Vector(0, -18, -20)
ss_l = make_strut(p_ss_start_l, p_dropout_l, ss_od)
ss_r = make_strut(p_ss_start_r, p_dropout_r, ss_od)

# 8. Dropouts
dropout_l = cq.Solid.makeCylinder(dropout_od / 2.0, 10, p_dropout_l - cq.Vector(0, 5, 0), cq.Vector(0, 1, 0))
dropout_r = cq.Solid.makeCylinder(dropout_od / 2.0, 10, p_dropout_r - cq.Vector(0, 5, 0), cq.Vector(0, 1, 0))

# 9. Bridges
# Chain Stay Bridge
bridge_pct_cs = 0.15
p_br_cs_l = p_cs_start_l + (p_dropout_l - p_cs_start_l) * bridge_pct_cs
p_br_cs_r = p_cs_start_r + (p_dropout_r - p_cs_start_r) * bridge_pct_cs
cs_bridge = make_strut(p_br_cs_l, p_br_cs_r, 14.0)

# Seat Stay Bridge
bridge_pct_ss = 0.20
p_br_ss_l = p_ss_start_l + (p_dropout_l - p_ss_start_l) * bridge_pct_ss
p_br_ss_r = p_ss_start_r + (p_dropout_r - p_ss_start_r) * bridge_pct_ss
ss_bridge = make_strut(p_br_ss_l, p_br_ss_r, 12.0)

# --- Assembly ---
parts = [
    seat_tube, head_tube, top_tube, down_tube,
    cs_l, cs_r, ss_l, ss_r,
    dropout_l, dropout_r,
    cs_bridge, ss_bridge
]

# Start with BB and fuse everything else
result = cq.Workplane(obj=bb_shell)

for part in parts:
    result = result.union(cq.Workplane(obj=part))