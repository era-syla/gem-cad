import cadquery as cq

# Base cylinder
base = cq.Workplane("XY").circle(20).extrude(30)

# Flange
flange = base.faces(">Z").workplane().rect(40, 40).extrude(5)

# Square ring on top of flange
outer = flange.faces(">Z").workplane().rect(40, 40).extrude(20)
inner_cut = flange.faces(">Z").workplane().rect(36, 36).extrude(20)
ring = outer.cut(inner_cut)

result = ring

# Spherical coupling with four radial holes
coupling = cq.Workplane("XY").sphere(12)
for angle in [0, 90, 180, 270]:
    hole = (
        cq.Workplane("XY")
        .circle(3)
        .extrude(50)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    coupling = coupling.cut(hole)
coupling = coupling.translate((0, 0, 30 + 5 + 20 + 12))
result = result.union(coupling)

# Hexagonal shaft through the coupling
shaft = (
    cq.Workplane("XY")
    .polygon(6, 4)
    .extrude(50)
    .translate((0, 0, 30 + 5 + 20))
)
result = result.union(shaft)

# Four mounting screws (simple cylinders) at corners of the ring
for x in (-15, 15):
    for y in (-15, 15):
        screw = (
            cq.Workplane("XY")
            .workplane(offset=30 + 5 + 20)
            .center(x, y)
            .circle(2)
            .extrude(40)
        )
        result = result.union(screw)