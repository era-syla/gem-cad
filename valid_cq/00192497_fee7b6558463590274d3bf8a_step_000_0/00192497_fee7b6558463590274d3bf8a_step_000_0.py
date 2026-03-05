import cadquery as cq

# --- Parameters ---
# Geometric dimensions
radius_center = 50.0       # Radius of the arc centerline
arm_width = 15.0           # Width of the arm (Z-height)
arm_thickness = 4.0        # Radial thickness of the arm
mount_radius = 7.5         # Radius of the mount cylinders (15mm diameter)
mount_hole_radius = 2.5    # Radius of the screw hole (5mm diameter)
nut_hex_diameter = 9.2     # Circumscribed diameter for M5 nut (approx 8mm across flats)
nut_depth = 3.5            # Depth of the hex recess
prong_gap = 3.0            # Width of the gaps between prongs
prong_thickness = 3.0      # Thickness of the prongs

# Calculated parameters to align arm outer surface with mount outer surface
# Arm outer radius matches the mount's outer tangent
arm_outer_radius = radius_center + mount_radius 
arm_inner_radius = arm_outer_radius - arm_thickness

# Positions for the mounts (90 degree separation)
pos_mount_1 = (radius_center, 0)
pos_mount_2 = (0, radius_center)

# --- Modeling ---

# 1. Create the Curved Arm Body
# We create a ring and keep the first quadrant
arm = (
    cq.Workplane("XY")
    .circle(arm_outer_radius)
    .circle(arm_inner_radius)
    .extrude(arm_width)
)

# Cut the ring to get the 90-degree sector
# Use an intersection with a box in the first quadrant
# Box dimensions cover the entire potential area
box_size = arm_outer_radius * 2.5
cutter_box = (
    cq.Workplane("XY")
    .box(box_size, box_size, arm_width * 2)
    .translate((box_size/2, box_size/2, 0))
)
arm = arm.intersect(cutter_box)

# 2. Create the Mount Knuckles (Cylinders)
# Knuckle 1 (Bottom/Horizontal end)
knuckle_1 = (
    cq.Workplane("XY")
    .moveTo(*pos_mount_1)
    .circle(mount_radius)
    .extrude(arm_width)
)

# Knuckle 2 (Top/Vertical end)
knuckle_2 = (
    cq.Workplane("XY")
    .moveTo(*pos_mount_2)
    .circle(mount_radius)
    .extrude(arm_width)
)

# Union the parts
result = arm.union(knuckle_1).union(knuckle_2)

# 3. Add Smooth Transitions (Fillets)
# Fillet the inner vertical edges where the arm meets the knuckles.
# We select edges parallel to Z, on the inner side (distance to origin < arm_inner_radius)
try:
    result = result.edges("|Z").filter(
        lambda e: e.Center().Length < arm_inner_radius + 1.0
    ).fillet(5.0)
except Exception:
    # Fallback if fillet fails (e.g. geometry issues), though usually robust here
    pass

# 4. Machining: Through Holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([pos_mount_1, pos_mount_2])
    .circle(mount_hole_radius)
    .cutThruAll()
)

# 5. Machining: GoPro Style Prongs
# Mount 1 (Bottom, at Y=0): 2-Prong configuration
# This fits into a 3-prong mount.
# 3-prong has tabs at Z=[0-3], [6-9], [12-15]
# So 2-prong must have tabs at Z=[3-6], [9-12]
# We remove material at Z=[0-3], [6-9], [12-15]
cut_ranges_2prong = [(0, 3), (6, 9), (12, 15)]

for z_start, z_end in cut_ranges_2prong:
    z_center = (z_start + z_end) / 2.0
    h_cut = z_end - z_start
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=z_center - h_cut/2)
        .moveTo(*pos_mount_1)
        .circle(mount_radius + 0.1) # Slightly oversize to ensure clean cut edges
        .extrude(h_cut)
    )
    result = result.cut(cutter)

# Mount 2 (Top, at X=0): 3-Prong configuration
# Standard mount. Tabs at Z=[0-3], [6-9], [12-15]
# We remove material at Z=[3-6], [9-12]
cut_ranges_3prong = [(3, 6), (9, 12)]

for z_start, z_end in cut_ranges_3prong:
    z_center = (z_start + z_end) / 2.0
    h_cut = z_end - z_start
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=z_center - h_cut/2)
        .moveTo(*pos_mount_2)
        .circle(mount_radius + 0.1)
        .extrude(h_cut)
    )
    result = result.cut(cutter)

# 6. Machining: Hex Nut Recess
# On the 3-Prong side (Mount 2), typically on the outer face
result = (
    result.faces(">Z")
    .workplane()
    .moveTo(*pos_mount_2)
    .polygon(6, nut_hex_diameter)
    .cutBlind(-nut_depth)
)

# Final Result is stored in 'result'