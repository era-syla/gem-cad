import cadquery as cq

# Create the base block
base = cq.Workplane("XY").box(40, 20, 5)

# Create the semi-circular arch area
arch = cq.Workplane("XY").workplane(offset=5).center(0, 0).circle(10).extrude(10)

# Cut the semi-circular arch
result = base.union(arch).cut(
    cq.Workplane("XY").workplane(offset=5).center(0, 0).circle(7).extrude(10)
)

# Create holes
result = result.faces(">Z").workplane().pushPoints([(-10, 0), (10, 0), (0, 10)]).hole(3)

# Create the slot
slot_cut = (
    cq.Workplane("XY")
    .workplane(offset=5)
    .center(0, 0)
    .rect(20, 10)
    .extrude(5, combine=False)
)

# Combine the parts and make the final cut
result = result.cut(slot_cut)