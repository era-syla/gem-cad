import cadquery as cq

# Parametric dimensions
L = 100.0        # Total length
H = 40.0         # Total height
D = 20.0         # Total depth/thickness

# Groove dimensions (runs along the bottom back)
groove_y = 20.0  # Height of the bottom groove
groove_z = 6.0   # Depth of the groove
groove_offset_z = 4.0 # Distance from the back face

# Front pocket features (creates the stepped surface and interlocking shape)
pocket_depth = 8.0 # Depth of the cutout from the front face
left_pad_w = 40.0  # Width of the thick bottom-left pad
channel_w = 12.0   # Width of the vertical channel

# Hole dimensions
hole_radius = 3.5
hole_offset_x = 15.0

# 1. Create main solid body
base = cq.Workplane("XY").box(L, H, D, centered=(False, False, False))

# 2. Cut the longitudinal bottom groove
groove = (
    cq.Workplane("XY")
    .workplane(offset=groove_offset_z)
    .box(L, groove_y, groove_z, centered=(False, False, False))
)

# 3. Cut the top-left front recessed area
pocket1 = (
    cq.Workplane("XY")
    .workplane(offset=D - pocket_depth)
    .center(0, groove_y)
    .box(left_pad_w, H - groove_y, pocket_depth, centered=(False, False, False))
)

# 4. Cut the middle vertical channel
pocket2 = (
    cq.Workplane("XY")
    .workplane(offset=D - pocket_depth)
    .center(left_pad_w, 0)
    .box(channel_w, groove_y, pocket_depth, centered=(False, False, False))
)

# 5. Create the holes
hole_pts = [
    (hole_offset_x, 10),               # Bottom-left hole
    (hole_offset_x, 30),               # Top-left hole
    (L - hole_offset_x, 30)            # Top-right hole
]
holes = (
    cq.Workplane("XY")
    .pushPoints(hole_pts)
    .circle(hole_radius)
    .extrude(D)
)

# Combine operations
result = base - groove - pocket1 - pocket2 - holes