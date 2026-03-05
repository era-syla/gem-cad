import cadquery as cq

# Main body dimensions
body_w = 60
body_d = 50
body_h = 40

# Create the main rectangular base body
base = cq.Workplane("XY").box(body_w, body_d, body_h, centered=(True, True, False))

# Cut the angled front-right corner (diagonal cut)
# The cut removes the front-right corner with a diagonal plane
# We'll use a triangular prism cut on the front-right
cut_pts = [
    (body_w/2, -body_d/2, -1),
    (body_w/2, 0, -1),
    (0, -body_d/2, -1),
]

# Create angled body: start with box, cut diagonal corner
# The shape looks like a box with one corner cut diagonally (front-left area)
# and a slot cut from the bottom-front

# Build the profile in XY plane (top view)
# Rectangle minus one triangular corner
profile = (
    cq.Workplane("XY")
    .moveTo(-body_w/2, -body_d/2)
    .lineTo(body_w/2, -body_d/2)
    .lineTo(body_w/2, body_d/2)
    .lineTo(-body_w/2 + 15, body_d/2)
    .lineTo(-body_w/2, body_d/2 - 15)
    .lineTo(-body_w/2, -body_d/2)
    .close()
    .extrude(body_h)
)

# Actually let's do a simpler approach matching the image:
# Box with diagonal cut on front-left top corner region
# Image shows: rectangular block, diagonal cut on one top corner,
# a circular hole/boss on right side, slot cut on left side bottom

# Rebuild cleanly
W = 60
D = 55
H = 38

# Main body - box
result = cq.Workplane("XY").box(W, D, H, centered=(True, True, False))

# Diagonal cut on the front-left corner (viewed from top)
# Cut a triangular prism
cut_plane = cq.Workplane("XY").workplane(offset=H)
diag_cut = (
    cq.Workplane("XY")
    .moveTo(-W/2, D/2)
    .lineTo(-W/2 + 20, D/2)
    .lineTo(-W/2, D/2 - 20)
    .close()
    .extrude(H + 2)
)
result = result.cut(diag_cut)

# Circular hole (cylindrical bore) on the right side
# The hole goes through in Y direction on the right portion
cyl_x = W/4
cyl_z = H * 0.6
cyl_r_outer = 12
cyl_r_inner = 8

# Boss/ring on right - cylinder going through in Y
result = (result
    .faces(">Y")
    .workplane()
    .center(-W/4 + 5, cyl_z - H/2)
    .hole(cyl_r_inner * 2, D)
)

# Slot cut on the left side bottom - U-shaped slot
slot_w = 14
slot_h = 20
slot_depth = 25

slot = (
    cq.Workplane("XY")
    .moveTo(-W/2 - 1, 0)
    .rect(slot_depth + 1, slot_w)
    .extrude(slot_h)
)
# Position slot at left side, bottom
slot = slot.translate((-W/2 + slot_depth/2 - 1, 0, 0))
result = result.cut(slot)

# Vertical wall slot - the image shows a rectangular slot from front
# Cut a slot from the front face going inward on left side
slot2 = (
    cq.Workplane("XY")
    .moveTo(-W/2 + slot_depth/2, -D/2)
    .rect(slot_depth, slot_w)
    .extrude(slot_h)
)
result = result.cut(slot2)