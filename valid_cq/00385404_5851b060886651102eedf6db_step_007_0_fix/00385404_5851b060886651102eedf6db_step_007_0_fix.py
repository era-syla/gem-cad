import cadquery as cq

# Create the base profile with a rounded end
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(20, 0)
    .lineTo(20, 100)
    .threePointArc((10, 110), (0, 100))
    .close()
    .extrude(3)
)

# Create holes along the length
holes = (
    base.faces(">Z")
    .workplane()
    .rarray(0, 12, 1, 8)
    .rect(3, 3)
    .cutThruAll()
)

result = base.union(holes)