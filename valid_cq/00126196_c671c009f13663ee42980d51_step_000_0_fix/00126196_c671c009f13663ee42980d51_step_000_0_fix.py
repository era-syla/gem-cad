import cadquery as cq

# Cylinder with two torus loops
cyl = cq.Workplane("XY").circle(15).extrude(10)

tor1 = (
    cq.Workplane("XZ")
    .center(22, 0)
    .circle(1.5)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)

tor2 = (
    cq.Workplane("XZ")
    .center(27, 0)
    .circle(1.5)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)

# Bracket: main vertical beam
bracket_main = (
    cq.Workplane("XY")
    .transformed(offset=(40, 0, 0))
    .rect(4, 4)
    .extrude(40)
)

# Bracket: angled side beam
bracket_side = (
    cq.Workplane("XY")
    .transformed(offset=(40, 0, 10), rotate=(0, 30, 0))
    .rect(4, 4)
    .extrude(30)
)

result = cyl.union(tor1).union(tor2).union(bracket_main).union(bracket_side)