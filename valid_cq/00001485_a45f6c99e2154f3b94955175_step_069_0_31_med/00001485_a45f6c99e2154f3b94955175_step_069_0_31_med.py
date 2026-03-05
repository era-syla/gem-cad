import cadquery as cq

# Parameters
L = 16.0
H = 12.0
T = 2.0
outer_W1 = 12.0
outer_W2 = 16.4

# ==========================================
# MALE PART (Left)
# ==========================================

# Base Plate
base1 = cq.Workplane("XY").box(L, outer_W1, T, centered=(False, True, False))
hole_base1 = cq.Workplane("XY").workplane(offset=-0.5).center(4, 0).circle(1.5).extrude(T + 1)
base1 = base1.cut(hole_base1)

# Right Side Plate (+Y)
offset_R1 = outer_W1 / 2 - T
sp_R1 = cq.Workplane("XZ").workplane(offset=offset_R1).box(L, H, T, centered=(False, False, False))
cyl_R1 = cq.Workplane("XZ").workplane(offset=offset_R1).center(L, H / 2).circle(H / 2).extrude(T)
sp_R1 = sp_R1.union(cyl_R1)

cutout_R1 = cq.Workplane("XZ").workplane(offset=offset_R1 - 0.5).center(L / 2, H / 2).box(4, 6, T + 1, centered=(True, True, False))
sp_R1 = sp_R1.cut(cutout_R1)

pin_R1 = cq.Workplane("XZ").workplane(offset=offset_R1 + T).center(L, H / 2).circle(2).extrude(2)
sp_R1 = sp_R1.union(pin_R1)

# Left Side Plate (-Y)
offset_L1 = -outer_W1 / 2
sp_L1 = cq.Workplane("XZ").workplane(offset=offset_L1).box(L, H, T, centered=(False, False, False))
cyl_L1 = cq.Workplane("XZ").workplane(offset=offset_L1).center(L, H / 2).circle(H / 2).extrude(T)
sp_L1 = sp_L1.union(cyl_L1)

cutout_L1 = cq.Workplane("XZ").workplane(offset=offset_L1 - 0.5).center(L / 2, H / 2).box(4, 6, T + 1, centered=(True, True, False))
sp_L1 = sp_L1.cut(cutout_L1)

pin_L1 = cq.Workplane("XZ").workplane(offset=offset_L1).center(L, H / 2).circle(2).extrude(-2)
sp_L1 = sp_L1.union(pin_L1)

# T-Tab (Left End)
tab_beam1 = cq.Workplane("XY").center(-4, 0).box(8, 4, T, centered=(True, True, False))
tab_head1 = cq.Workplane("XY").center(-9, 0).box(2, 8, T, centered=(True, True, False))
bump1 = cq.Workplane("XY").center(-9, 0).cylinder(T + 1, 1.2, centered=(True, True, False))
tab1 = tab_beam1.union(tab_head1).union(bump1)

# Combine Male Part
male = base1.union(sp_R1).union(sp_L1).union(tab1)


# ==========================================
# FEMALE PART (Right)
# ==========================================

# Base Plate
base2 = cq.Workplane("XY").box(L, outer_W2, T, centered=(False, True, False))
hole_base2 = cq.Workplane("XY").workplane(offset=-0.5).center(L - 4, 0).circle(1.5).extrude(T + 1)
base2 = base2.cut(hole_base2)

# Right Side Plate (+Y)
offset_R2 = outer_W2 / 2 - T
sp_R2 = cq.Workplane("XZ").workplane(offset=offset_R2).box(L, H, T, centered=(False, False, False))
cyl_R2 = cq.Workplane("XZ").workplane(offset=offset_R2).center(0, H / 2).circle(H / 2).extrude(T)
sp_R2 = sp_R2.union(cyl_R2)

cutout_R2 = cq.Workplane("XZ").workplane(offset=offset_R2 - 0.5).center(L / 2, H / 2).box(4, 6, T + 1, centered=(True, True, False))
sp_R2 = sp_R2.cut(cutout_R2)

hole_R2 = cq.Workplane("XZ").workplane(offset=offset_R2 - 0.5).center(0, H / 2).circle(2.2).extrude(T + 1)
sp_R2 = sp_R2.cut(hole_R2)

# Left Side Plate (-Y)
offset_L2 = -outer_W2 / 2
sp_L2 = cq.Workplane("XZ").workplane(offset=offset_L2).box(L, H, T, centered=(False, False, False))
cyl_L2 = cq.Workplane("XZ").workplane(offset=offset_L2).center(0, H / 2).circle(H / 2).extrude(T)
sp_L2 = sp_L2.union(cyl_L2)

cutout_L2 = cq.Workplane("XZ").workplane(offset=offset_L2 - 0.5).center(L / 2, H / 2).box(4, 6, T + 1, centered=(True, True, False))
sp_L2 = sp_L2.cut(cutout_L2)

hole_L2 = cq.Workplane("XZ").workplane(offset=offset_L2 - 0.5).center(0, H / 2).circle(2.2).extrude(T + 1)
sp_L2 = sp_L2.cut(hole_L2)

# T-Tab (Right End)
tab_beam2 = cq.Workplane("XY").center(L + 4, 0).box(8, 4, T, centered=(True, True, False))
tab_head2 = cq.Workplane("XY").center(L + 9, 0).box(2, 8, T, centered=(True, True, False))
bump2 = cq.Workplane("XY").center(L + 9, 0).cylinder(T + 1, 1.2, centered=(True, True, False))
tab2 = tab_beam2.union(tab_head2).union(bump2)

# Combine Female Part
female = base2.union(sp_R2).union(sp_L2).union(tab2)

# Position Female part nicely next to Male part
female = female.rotate((0, 0, 0), (0, 0, 1), 15).translate((35, 10, 0))

# ==========================================
# FINAL ASSEMBLY
# ==========================================

result = male.union(female)