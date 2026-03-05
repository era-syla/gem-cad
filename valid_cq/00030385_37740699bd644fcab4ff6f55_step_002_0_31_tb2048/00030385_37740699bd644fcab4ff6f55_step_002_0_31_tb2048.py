import cadquery as cq

# Fuselage
fuselage = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(105, 0)
    .lineTo(105, 10)
    .lineTo(20, 10)
    .lineTo(0, 3)
    .close()
    .extrude(5, both=True)
)

# Main Wing
wing = (
    cq.Workplane("XZ")
    .moveTo(45, 10)
    .lineTo(20, 10)
    .threePointArc((27, 13.5), (45, 10))
    .close()
    .extrude(120, both=True)
)

# Horizontal Stabilizer
tail_wing = (
    cq.Workplane("XZ")
    .moveTo(95, 10)
    .lineTo(85, 10)
    .threePointArc((88, 11.5), (95, 10))
    .close()
    .extrude(25, both=True)
)

# Vertical Stabilizer
vert_stab = (
    cq.Workplane("XZ")
    .moveTo(85, 10)
    .lineTo(95, 10)
    .lineTo(98, 25)
    .lineTo(91, 25)
    .close()
    .extrude(1.5, both=True)
)

# Combine all components into the final geometry
result = fuselage.union(wing).union(tail_wing).union(vert_stab)