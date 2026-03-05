import cadquery as cq

# Fuselage parameters
fuse_len = 160
fuse_width = 14
fuse_height = 14
nose_slope_start = -50

# Wing parameters
wing_span = 360
wing_chord = 40
wing_thick = 4.5
wing_le_x = -40
wing_te_x = wing_le_x + wing_chord

# Horizontal stabilizer parameters
hstab_span = 90
hstab_chord = 25
hstab_thick = 2
hstab_te_x = 80
hstab_le_x = hstab_te_x - hstab_chord

# Vertical stabilizer parameters
vstab_root_chord = 20
vstab_tip_chord = 10
vstab_height = 25
vstab_thick = 2

# 1. Fuselage
fuse_profile = (
    cq.Workplane("XZ")
    .moveTo(-fuse_len/2, -fuse_height/2)
    .lineTo(fuse_len/2, -fuse_height/2)
    .lineTo(fuse_len/2, fuse_height/2)
    .lineTo(nose_slope_start, fuse_height/2)
    .lineTo(-fuse_len/2, 0)
    .close()
)
fuselage = fuse_profile.extrude(fuse_width/2, both=True)

# 2. Main Wing
wing_profile = (
    cq.Workplane("XZ")
    .moveTo(wing_le_x, fuse_height/2)
    .lineTo(wing_te_x, fuse_height/2)
    .lineTo(wing_te_x, fuse_height/2 + 0.5)
    .threePointArc(
        (wing_le_x + wing_chord * 0.3, fuse_height/2 + wing_thick),
        (wing_le_x, fuse_height/2)
    )
    .close()
)
wing = wing_profile.extrude(wing_span/2, both=True)

# 3. Horizontal Stabilizer
hstab_profile = (
    cq.Workplane("XZ")
    .moveTo(hstab_le_x, fuse_height/2)
    .lineTo(hstab_te_x, fuse_height/2)
    .lineTo(hstab_te_x, fuse_height/2 + hstab_thick)
    .lineTo(hstab_le_x, fuse_height/2 + hstab_thick)
    .close()
)
hstab = hstab_profile.extrude(hstab_span/2, both=True)

# 4. Vertical Stabilizer
vstab_profile = (
    cq.Workplane("XZ")
    .moveTo(hstab_te_x - vstab_root_chord, fuse_height/2 + hstab_thick)
    .lineTo(hstab_te_x, fuse_height/2 + hstab_thick)
    .lineTo(hstab_te_x, fuse_height/2 + hstab_thick + vstab_height)
    .lineTo(hstab_te_x - vstab_tip_chord, fuse_height/2 + hstab_thick + vstab_height)
    .close()
)
vstab = vstab_profile.extrude(vstab_thick/2, both=True)

# Combine all components
result = fuselage.union(wing).union(hstab).union(vstab)