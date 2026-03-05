import cadquery as cq

# Parametric dimensions
L = 160.0
H = 15.0
T_front = 5.0

block_L = 20.0
block_D = 12.0
block_dist = 90.0

slot_dist = 135.0
slot_len = 8.0
slot_w = 4.0

hole_dia = 8.0
slit_w = 1.0
screw_dia = 3.0

# 1. Base front bar
# Centered at origin along X and Z, back face flush with XZ plane (Y=0)
front_bar = cq.Workplane("XY").center(0, -T_front/2).box(L, T_front, H)

# 2. Rear mounting blocks
# Attach to the back of the front bar (from Y=0 to Y=block_D)
blocks = (
    cq.Workplane("XY")
    .pushPoints([(block_dist/2, block_D/2), (-block_dist/2, block_D/2)])
    .box(block_L, block_D, H)
)
result = front_bar.union(blocks)

# 3. Mounting slots on the front bar
# Selected from the front face (Y = -T_front)
result = (
    result.faces("<Y").workplane()
    .pushPoints([(slot_dist/2, 0), (-slot_dist/2, 0)])
    .slot2D(slot_len, slot_w, 0)
    .cutBlind(-T_front - 2)
)

# 4. Vertical clamping holes in the rear blocks
# Selected from the top face
result = (
    result.faces(">Z").workplane()
    .pushPoints([(block_dist/2, block_D/2), (-block_dist/2, block_D/2)])
    .hole(hole_dia)
)

# 5. Clamping slits
# Cuts from the center of the vertical holes to the back face
result = (
    result.faces(">Z").workplane()
    .pushPoints([(block_dist/2, block_D), (-block_dist/2, block_D)])
    .rect(slit_w, block_D + 2)
    .cutBlind(-H - 2)
)

# 6. Clamp screw holes
# A longitudinal cut along the X-axis crossing the slits to allow clamping
screw_cut = (
    cq.Workplane("YZ")
    .center(block_D/2, 0)
    .circle(screw_dia/2)
    .extrude(L/2, both=True)
)
result = result.cut(screw_cut)