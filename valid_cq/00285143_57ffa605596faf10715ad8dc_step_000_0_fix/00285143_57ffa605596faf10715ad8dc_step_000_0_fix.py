import cadquery as cq

# Base part
base = cq.Workplane("XY").box(40, 40, 10)

# U-shape cut
cutout = (
    cq.Workplane("XY", origin=(0, 0, 10))
    .center(0, -10)
    .rect(30, 30)
    .extrude(-10)
)

# Remove cutout from base
result = base.cut(cutout)

# Arch section
arch = (
    cq.Workplane("XZ")
    .center(0, 20)
    .circle(20)
    .extrude(10)
)

# Remove bottom half to form arch
arch = arch.faces(">Y").workplane().split(keepBottom=True)

# Combine arch with result
result = result.union(arch)

# Holes in the base
result = result.faces("<Z").workplane().pushPoints([(-10, -10), (10, -10), (0, 0)]).hole(5)

# Fillets on edges
result = result.edges("|Z").fillet(2)