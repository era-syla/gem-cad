import cadquery as cq

# Main block: 30 mm wide (X), 20 mm thick (Y), 80 mm tall (Z), bottom at Z=0
main = cq.Workplane("XY").box(30, 20, 80, centered=(True, True, False))

# Add a half-cylinder “arch” on top, 30 mm span, 15 mm rise, spanning the full 20 mm thickness
arch = (
    cq.Workplane("XZ", origin=(0, 0, 80))
    .moveTo(-15, 0)
    .threePointArc((0, 15), (15, 0))
    .close()
    .extrude(20)
    .translate((0, -10, 0))
)

# Build an elbow fitting: horizontal cylinder through the right face, then vertical stub
# Horizontal cylinder (outer Ø6, inner Ø5), 20 mm long, centered at mid-height
cyl1 = (
    cq.Workplane("YZ", origin=(15, 0, 40))
    .circle(3)     # outer
    .circle(2.5)   # inner
    .extrude(20)
)

# Vertical stub (outer Ø6, inner Ø5), 20 mm tall, at end of horizontal piece
cyl2 = (
    cq.Workplane("XY", origin=(35, 0, 40))
    .circle(3)
    .circle(2.5)
    .extrude(20)
)

result = main.union(arch).union(cyl1).union(cyl2)