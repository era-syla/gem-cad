import cadquery as cq

# Parameters
R = 15       # arch radius
T = 5        # base thickness
L_plate = 20 # length of mounting plate on the left
L_arch = 40  # length of the arch section
L_prong = 20 # length of the prong section on the right
W = 2 * R    # total width
H = T + R    # total height
gap = 10     # slot width in prong section

# Base block
result = cq.Workplane("XY").box(L_plate + L_arch + L_prong, W, T)

# Arch (semi‐cylinder)
arch_full = (
    cq.Workplane("YZ", origin=(L_plate, 0, T + R))  # center circle at z = T+R
      .circle(R)
      .extrude(L_arch)                              # extrude along +X
)
# Cutter to remove top half of the full cylinder (keep bottom half)
arch_cutter = (
    cq.Workplane("XY", origin=(L_plate + L_arch/2, 0, T + R))  # plane at mid‐height of full cylinder
      .box(L_arch + 2, W + 2, R)                               # box taller than R to cut top half
)
arch = arch_full.cut(arch_cutter)
result = result.union(arch)

# Left mounting plate (rises to the top of the arch)
plate = (
    cq.Workplane("XY", origin=(L_plate/2, 0, T + R/2))
      .box(L_plate, W, R)
)
result = result.union(plate)

# Slot cut on prong side to form two vertical prongs
slot_cutter = (
    cq.Workplane("XY", origin=(L_plate + L_arch + L_prong/2, 0, H/2))
      .box(L_prong, gap, H)
)
result = result.cut(slot_cutter)

# Create holes from the top face
wp = result.faces(">Z").workplane()

# Two mounting holes in the left plate
plate_hole_spacing = 8
plate_holes = [
    (L_plate/2 - plate_hole_spacing/2, 0),
    (L_plate/2 + plate_hole_spacing/2, 0),
]
result = wp.pushPoints(plate_holes).hole(4)

# Central hole through the arch
arch_hole_x = L_plate + L_arch/2 - (L_plate + L_arch + L_prong)/2  # shift into workplane coords
result = result.faces(">Z").workplane().pushPoints([(arch_hole_x, 0)]).hole(6)