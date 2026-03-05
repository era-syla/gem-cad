import cadquery as cq

# Create base box and cut a window
result = (
    cq.Workplane("XY")
    .box(60, 40, 30)
    .faces(">Y")
    .workplane()
    .rect(30, 15)
    .cutThruAll()
)

# Create a curved roof by extruding an arc profile
roof_profile = (
    cq.Workplane("XZ")
    .moveTo(-35, 0)
    .threePointArc((0, 15), (35, 0))
    .lineTo(-35, 0)
    .close()
)
roof = roof_profile.extrude(50).translate((0, -25, 30))
result = result.union(roof)

# Cut three long grooves into the roof
for x in (-20, 0, 20):
    cutter = (
        cq.Workplane("XY")
        .transformed(offset=(x, 0, 40))
        .box(5, 60, 30, centered=(True, True, False))
    )
    result = result.cut(cutter)