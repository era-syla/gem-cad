import cadquery as cq

# Build the part from bottom to top

# Bottom cylinder (short, wide)
bottom_cyl = (
    cq.Workplane("XY")
    .cylinder(8, 12)
)

# Stem cylinder above bottom
stem = (
    cq.Workplane("XY")
    .workplane(offset=8)
    .cylinder(20, 9)
)

# Cone (frustum) - transitions from stem to wider base plate area
# Using revolve to create a frustum
cone = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .transformed(offset=cq.Vector(0, 0, 28))
    .add(
        cq.Workplane("XY")
        .workplane(offset=28)
        .circle(9)
        .workplane(offset=18)
        .circle(18)
        .loft()
    )
)

# Let me rebuild more carefully using unions

# Base cylinder at bottom
part = cq.Workplane("XY").cylinder(8, 12)

# Add stem
part = part.union(
    cq.Workplane("XY").workplane(offset=4).cylinder(22, 9)
)

# Add frustum/cone transitioning upward
cone_solid = (
    cq.Workplane("XY")
    .workplane(offset=26)
    .circle(9)
    .workplane(offset=14)
    .circle(20)
    .loft()
)
part = part.union(cone_solid)

# Add flat base plate at top of cone
plate_z = 40
plate = (
    cq.Workplane("XY")
    .workplane(offset=plate_z)
    .box(50, 40, 6, centered=(True, True, False))
)
# Round corners of plate
plate = plate.edges("|Z").fillet(5)

part = part.union(plate)

# Add mounting tab/ear on side of plate
tab = (
    cq.Workplane("XY")
    .workplane(offset=plate_z)
    .transformed(offset=cq.Vector(20, 5, 0))
    .box(18, 18, 6, centered=(True, True, False))
)
tab = tab.edges("|Z").fillet(3)

part = part.union(tab)

# Hole in mounting tab
tab_hole = (
    cq.Workplane("XY")
    .workplane(offset=plate_z - 1)
    .transformed(offset=cq.Vector(20, 5, 0))
    .circle(4)
    .extrude(10)
)
part = part.cut(tab_hole)

# Add threaded/ridged cone on top (screw tip)
# Create stacked diminishing cylinders to simulate thread
screw_base_z = plate_z + 6
screw_parts = []

# Main screw cone
screw_cone = (
    cq.Workplane("XY")
    .workplane(offset=screw_base_z)
    .circle(10)
    .workplane(offset=30)
    .circle(1.5)
    .loft()
)
part = part.union(screw_cone)

# Add thread rings around the screw cone
num_threads = 8
for i in range(num_threads):
    frac = i / num_threads
    z_pos = screw_base_z + frac * 28
    r_outer = 10 * (1 - frac) + 1.5 * frac
    ring_r = r_outer + 1.5 * (1 - frac)
    ring = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .circle(ring_r)
        .workplane(offset=2.5)
        .circle(ring_r - 1.5)
        .loft()
    )
    part = part.union(ring)

# Add slot/notch at tip
tip_z = screw_base_z + 30
slot = (
    cq.Workplane("XY")
    .workplane(offset=tip_z - 4)
    .rect(1.5, 6)
    .extrude(6)
)
part = part.cut(slot)

result = part