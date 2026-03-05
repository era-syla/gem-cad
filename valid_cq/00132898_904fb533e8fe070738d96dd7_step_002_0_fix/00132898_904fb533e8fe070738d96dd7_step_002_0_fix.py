import cadquery as cq

# Base triangular plate with holes
base = (
    cq.Workplane("XY")
    .polygon(3, 120)
    .extrude(3)
    .faces(">Z")
    .workplane()
    .pushPoints([(-40, 40), (0, 60), (40, 40), (0, 30)])
    .circle(5)
    .cutThruAll()
)

# Cylindrical supports
cylinder1 = cq.Workplane("XY").center(-60, 0).circle(7).extrude(60)
cylinder2 = cq.Workplane("XY").center(60, 0).circle(7).extrude(60)

# Create the lower triangular plate with holes
lower_base = (
    cq.Workplane("XY")
    .polygon(3, 120)
    .extrude(3)
    .faces(">Z")
    .workplane()
    .pushPoints([(-40, 40), (0, 60), (40, 40), (0, 30)])
    .circle(5)
    .cutThruAll()
    .translate((0, 0, -40))
)

# Small connector plate
connector = (
    cq.Workplane("XY")
    .polygon(3, 60)
    .extrude(30)
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 20)])
    .circle(3)
    .cutBlind(-10)
    .translate((0, 0, -80))
)

result = base.union(cylinder1).union(cylinder2).union(lower_base).union(connector)