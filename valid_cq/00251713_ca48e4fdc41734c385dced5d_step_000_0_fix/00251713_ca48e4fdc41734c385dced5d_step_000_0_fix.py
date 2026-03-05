import cadquery as cq

# Base triangular plate
base = cq.Workplane("XY") \
    .polyline([(0, 0), (120, 0), (0, 100)]) \
    .close() \
    .extrude(6)

# Corner supports
support1 = cq.Workplane("XY").box(10, 10, 20).translate((10, 10, 6))
support2 = cq.Workplane("XY").box(10, 10, 20).translate((110, 10, 6))
support3 = cq.Workplane("XY").box(10, 10, 20).translate((10, 90, 6))

# Vertical column with top hole
column = (
    cq.Workplane("XY")
    .rect(20, 20)
    .extrude(60)
    .faces(">Z")
    .workplane()
    .hole(10)
    .translate((60, 30, 6))
)

# Linear rail
rail = cq.Workplane("XY").box(5, 5, 80).translate((60, 30, 26))

# Carriage block
carriage = cq.Workplane("XY").box(25, 15, 10).translate((60, 30, 26 + 35))

# Left beam bracket
beam = (
    cq.Workplane("XY")
    .box(10, 10, 100)
    .rotate((0, 0, 0), (0, 0, 1), 90)
    .translate((150, 0, 25))
)

# Combine all parts
result = (
    base
    .union(support1)
    .union(support2)
    .union(support3)
    .union(column)
    .union(rail)
    .union(carriage)
    .union(beam)
)