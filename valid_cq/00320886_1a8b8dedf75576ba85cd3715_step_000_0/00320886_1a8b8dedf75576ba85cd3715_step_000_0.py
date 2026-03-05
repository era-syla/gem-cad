import cadquery as cq

# Parameters for component dimensions
# 1. Central Housing (Pillow Block / Nut Housing)
housing_width = 30
housing_depth = 25
housing_height = 25
housing_bore = 16
housing_mount_hole_d = 3.5
housing_mount_spacing = 20

# 2. Tall Sleeve (Linear Bearing)
sleeve_od = 15
sleeve_id = 10
sleeve_height = 30

# 3. Short Spacer
spacer_od = 18
spacer_id = 10
spacer_height = 12

# 4. T-Bracket
bracket_plate_w = 36
bracket_plate_t = 5
bracket_plate_h = 12
bracket_block_w = 14
bracket_block_d = 15
bracket_hole_d = 6

# 5. End Cap (D-shape)
cap_plate_w = 40
cap_plate_t = 5
cap_plate_h = 15
cap_block_w = 20
cap_block_d = 15

# --- Geometry Creation ---

# 1. Create Central Housing
# Centered at (0,0,0)
housing = (
    cq.Workplane("XY")
    .box(housing_width, housing_depth, housing_height)
    .faces(">Z").workplane()
    .hole(housing_bore)
    .faces("<Y").workplane()
    .pushPoints([(-housing_mount_spacing/2, 0), (housing_mount_spacing/2, 0)])
    .hole(housing_mount_hole_d, depth=10)
)

# 2. Create Tall Sleeve
# Positioned top-right relative to center
sleeve = (
    cq.Workplane("XY")
    .circle(sleeve_od / 2)
    .circle(sleeve_id / 2)
    .extrude(sleeve_height)
    .translate((30, 35, 0))  # Offset position
)

# 3. Create Spacer
# Positioned left relative to center
spacer = (
    cq.Workplane("XY")
    .circle(spacer_od / 2)
    .circle(spacer_id / 2)
    .extrude(spacer_height)
    .translate((-35, 0, -housing_height/2 + spacer_height/2))
)

# 4. Create T-Bracket
# Positioned right relative to center
# Constructed from a plate and a block with a hole
bracket_block_geo = (
    cq.Workplane("XY")
    .box(bracket_block_w, bracket_block_d, bracket_plate_h)
    .faces(">Z").workplane()
    .hole(bracket_hole_d)
    .translate((0, bracket_block_d/2, 0))
)
bracket_plate_geo = (
    cq.Workplane("XY")
    .box(bracket_plate_w, bracket_plate_t, bracket_plate_h)
    .faces("<Y").workplane()
    .pushPoints([(-12, 0), (12, 0)])
    .hole(3)
    .translate((0, -bracket_plate_t/2, 0))
)
bracket = (
    bracket_block_geo.union(bracket_plate_geo)
    .translate((45, -15, -housing_height/2 + bracket_plate_h/2))
)

# 5. Create End Cap
# Positioned bottom-left relative to center
# Constructed from a plate and a radiused block
cap_plate_geo = (
    cq.Workplane("XY")
    .box(cap_plate_w, cap_plate_t, cap_plate_h)
    .translate((0, -cap_plate_t/2, 0))
)
cap_block_geo = (
    cq.Workplane("XY")
    .box(cap_block_w, cap_block_d, cap_plate_h)
    .faces(">Y").edges("|Z").fillet(cap_block_w/2 - 0.1) # Full fillet to create round end
    .translate((0, cap_block_d/2, 0))
)
cap = (
    cap_plate_geo.union(cap_block_geo)
    .translate((-20, -45, -housing_height/2 + cap_plate_h/2))
)

# --- Assembly ---

# Combine all disjoint solids into a single result object
result = (
    housing
    .union(sleeve)
    .union(spacer)
    .union(bracket)
    .union(cap)
)