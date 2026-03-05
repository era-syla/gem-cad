import cadquery as cq

# Base rectangular plate
plate = cq.Workplane("XY").box(80, 10, 3, centered=(True, True, False))

# Semi-circular arches
arch = (
    cq.Workplane("XY")
    .lineTo(26, 0)
    .threePointArc((40, 10), (54, 0))
    .close()
    .extrude(30)
)

# Combined shape
combined_shape = plate.union(arch)

# Cylindrical bosses on the ends
boss1 = (
    combined_shape.faces(">Y")
    .workplane(centerOption="CenterOfMass")
    .circle(5)
    .extrude(10, both=True)
)

boss2 = (
    combined_shape.faces("<Y")
    .workplane(centerOption="CenterOfMass")
    .circle(5)
    .extrude(10, both=True)
)

# Hole in the center of the bosses
boss_with_hole1 = boss1.faces(">Y").workplane(centerOption="CenterOfMass").circle(2).cutThruAll()
boss_with_hole2 = boss2.faces("<Y").workplane(centerOption="CenterOfMass").circle(2).cutThruAll()

# Final result
result = boss_with_hole1.union(boss_with_hole2)