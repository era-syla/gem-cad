import cadquery as cq

# Base plate
base = (
    cq.Workplane("XY")
    .rect(50, 75)
    .extrude(5)
    .faces(">Z")
    .workplane()
    .circle(12)
    .cutThruAll()
    .circle(4)
    .cutThruAll()
    .center(-20, 15)
    .rect(10, 20)
    .cutThruAll()
)

# Angle bracket
bracket = (
    cq.Workplane("XY")
    .center(0, 37.5)
    .rect(50, 5)
    .extrude(40)
    .faces(">Y")
    .workplane()
    .center(0, -37.5)
    .rect(5, 40)
    .extrude(-40)
    .edges(">Z")
    .fillet(2)
)

# Combine base and bracket
result = base.union(bracket)