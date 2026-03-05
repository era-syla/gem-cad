import cadquery as cq

# === Parameters ===
# Radii
bore_r = 6
endcap_l_r = 9
axle_l_r = 12
disc_flange_r_base = 18
disc_boss_r_center = 22
disc_boss_radius = 6
left_flange_r = 32
center_r = 16
right_flange_r = 34
freehub_r = 17.4
axle_r_r = 10
endcap_r_r = 8

# Z-axis positions (0 is left end)
Z_L_END = 0
Z_L_CAP = 6
Z_L_AXLE = 12
Z_DISC_1 = 14
Z_DISC_2 = 18
Z_L_FLANGE_1 = 26
Z_L_FLANGE_2 = 30
Z_CENTER = 55
Z_R_FLANGE_1 = 75
Z_R_FLANGE_2 = 79
Z_FREEHUB_END = 114
Z_R_AXLE = 118
Z_R_END = 125

# === Base Revolved Geometry ===
profile = (
    cq.Workplane("XZ")
    .moveTo(bore_r, Z_L_END)
    .lineTo(endcap_l_r - 1, Z_L_END)
    .lineTo(endcap_l_r, Z_L_END + 1)
    .lineTo(endcap_l_r, Z_L_CAP - 1)
    .lineTo(axle_l_r, Z_L_CAP + 1)
    .lineTo(axle_l_r, Z_L_AXLE)
    .lineTo(disc_flange_r_base, Z_DISC_1)
    .lineTo(disc_flange_r_base, Z_DISC_2)
    .lineTo(16, Z_DISC_2 + 2)
    .lineTo(16, Z_L_FLANGE_1 - 4)
    .spline([(22, Z_L_FLANGE_1 - 2), (left_flange_r - 2, Z_L_FLANGE_1)], includeCurrent=True)
    .lineTo(left_flange_r, Z_L_FLANGE_1 + 1)
    .lineTo(left_flange_r, Z_L_FLANGE_2 - 1)
    .lineTo(left_flange_r - 2, Z_L_FLANGE_2)
    .spline([(center_r, Z_CENTER), (right_flange_r - 2, Z_R_FLANGE_1)], includeCurrent=True)
    .lineTo(right_flange_r, Z_R_FLANGE_1 + 1)
    .lineTo(right_flange_r, Z_R_FLANGE_2 - 1)
    .lineTo(right_flange_r - 2, Z_R_FLANGE_2)
    .lineTo(freehub_r, Z_R_FLANGE_2 + 2)
    .lineTo(freehub_r, Z_FREEHUB_END - 1)
    .lineTo(freehub_r - 1, Z_FREEHUB_END)
    .lineTo(axle_r_r, Z_FREEHUB_END)
    .lineTo(axle_r_r, Z_R_AXLE - 1)
    .lineTo(endcap_r_r, Z_R_AXLE)
    .lineTo(endcap_r_r, Z_R_END - 1)
    .lineTo(endcap_r_r - 1, Z_R_END)
    .lineTo(bore_r, Z_R_END)
    .close()
)

hub = profile.revolve(360, (0, 0, 0), (0, 0, 1))

# === Disc Brake Mount Lobes ===
bosses = (
    cq.Workplane("XY", origin=(0, 0, Z_DISC_1))
    .polarArray(disc_boss_r_center, 0, 360, 6)
    .circle(disc_boss_radius)
    .extrude(Z_DISC_2 - Z_DISC_1)
)
hub = hub.union(bosses)

# === Holes ===
# Disc bolt holes
disc_holes = (
    cq.Workplane("XY").workplane(offset=Z_DISC_2)
    .polarArray(disc_boss_r_center, 0, 360, 6)
    .circle(2.5)
    .extrude(Z_DISC_2 - Z_DISC_1 + 2)
)
hub = hub.cut(disc_holes)

# Left spoke holes
left_spoke_holes = (
    cq.Workplane("XY").workplane(offset=Z_L_FLANGE_1 - 1)
    .polarArray(left_flange_r - 3, 0, 360, 16)
    .circle(1.3)
    .extrude(Z_L_FLANGE_2 - Z_L_FLANGE_1 + 2)
)
hub = hub.cut(left_spoke_holes)

# Right spoke holes
right_spoke_holes = (
    cq.Workplane("XY").workplane(offset=Z_R_FLANGE_1 - 1)
    .polarArray(right_flange_r - 3, 0, 360, 16)
    .circle(1.3)
    .extrude(Z_R_FLANGE_2 - Z_R_FLANGE_1 + 2)
)
hub = hub.cut(right_spoke_holes)

# === Freehub Splines ===
cut_dist = (Z_FREEHUB_END + 1) - (Z_R_FLANGE_2 + 2)
spline_cut = (
    cq.Workplane("XY", origin=(0, 0, Z_FREEHUB_END + 1))
    .polarArray(freehub_r, 0, 360, 9)
    .rect(3, 4) # Radial depth 3, circumferential width 4
    .extrude(-cut_dist)
)
hub = hub.cut(spline_cut)

# === Flange Support Ribs ===
# Left side ribs
left_rib_profile = (
    cq.Workplane("XZ")
    .moveTo(10, Z_L_FLANGE_2 - 1)
    .lineTo(left_flange_r - 2, Z_L_FLANGE_2 - 1)
    .lineTo(center_r + 1, Z_CENTER - 5)
    .lineTo(10, Z_CENTER - 5)
    .close()
)
left_rib = left_rib_profile.extrude(1.2, both=True)
try:
    left_rib = left_rib.edges("|Y").fillet(0.5)
except:
    pass # Robustness fallback

# Right side ribs
right_rib_profile = (
    cq.Workplane("XZ")
    .moveTo(10, Z_R_FLANGE_1 + 1)
    .lineTo(right_flange_r - 2, Z_R_FLANGE_1 + 1)
    .lineTo(center_r + 1, Z_CENTER + 5)
    .lineTo(10, Z_CENTER + 5)
    .close()
)
right_rib = right_rib_profile.extrude(1.2, both=True)
try:
    right_rib = right_rib.edges("|Y").fillet(0.5)
except:
    pass

# Pattern and unite ribs
for i in range(8):
    angle = i * 45
    hub = hub.union(left_rib.rotate((0, 0, 0), (0, 0, 1), angle))
    hub = hub.union(right_rib.rotate((0, 0, 0), (0, 0, 1), angle + 22.5))

# Final Result
result = hub