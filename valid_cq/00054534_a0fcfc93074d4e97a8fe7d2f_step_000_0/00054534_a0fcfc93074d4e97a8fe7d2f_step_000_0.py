import cadquery as cq

# --- Parameter Definitions ---
# Vertical Post dimensions
radius_vert = 8.0
height_vert = 50.0

# Horizontal Main Cylinder dimensions
radius_horiz = 6.0
length_horiz = 50.0  # Length from center to end
z_horiz = 10.0       # Height of horizontal intersection

# Stepped Stub dimensions (opposite to main cylinder)
stub_base_len = 10.0 # Distance from center to first step
stub_mid_rad = 5.0
stub_mid_len = 4.0
stub_tip_rad = 3.5
stub_tip_len = 3.0

# Thin Rod dimensions
radius_rod = 2.0
length_rod = 40.0    # Length from center
z_rod = 25.0         # Height of rod intersection

# --- Geometry Construction ---

# 1. Vertical Post (Centered on Z-axis)
post = (
    cq.Workplane("XY")
    .circle(radius_vert)
    .extrude(height_vert)
    .faces(">Z or <Z").chamfer(0.5)
)

# 2. Horizontal Long Arm (Extending in +X direction)
long_arm = (
    cq.Workplane("YZ", origin=(0, 0, z_horiz))
    .circle(radius_horiz)
    .extrude(length_horiz)
)

# 3. Stepped Stub (Extending in -X direction)
# Segment 1: Base extension from vertical post
stub_base = (
    cq.Workplane("YZ", origin=(0, 0, z_horiz))
    .circle(radius_horiz)
    .extrude(-stub_base_len)
)

# Segment 2: Middle stepped section
stub_mid = (
    cq.Workplane("YZ", origin=(-stub_base_len, 0, z_horiz))
    .circle(stub_mid_rad)
    .extrude(-stub_mid_len)
)

# Segment 3: Tip section
stub_tip = (
    cq.Workplane("YZ", origin=(-(stub_base_len + stub_mid_len), 0, z_horiz))
    .circle(stub_tip_rad)
    .extrude(-stub_tip_len)
)

# 4. Thin Side Rod (Extending in -Y direction)
# Using XZ plane (Normal is Y), moving origin to correct Z height
rod = (
    cq.Workplane("XZ", origin=(0, 0, z_rod))
    .circle(radius_rod)
    .extrude(-length_rod)
)

# --- Assembly ---
# Union all components
result = (
    post
    .union(long_arm)
    .union(stub_base)
    .union(stub_mid)
    .union(stub_tip)
    .union(rod)
)

# Add final detail: Chamfer on the tip of the stepped stub
result = result.faces("<X").chamfer(0.3)