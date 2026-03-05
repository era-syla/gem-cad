import cadquery as cq

# Main house body
main_body = (
    cq.Workplane("XY")
    .rect(80, 50)
    .extrude(30)
)

# Main roof (hip roof style) using a loft
roof_base = (
    cq.Workplane("XY")
    .workplane(offset=30)
    .rect(80, 50)
)

roof_top = (
    cq.Workplane("XY")
    .workplane(offset=48)
    .rect(60, 8)
)

main_roof = (
    cq.Workplane("XY")
    .workplane(offset=30)
    .rect(82, 52)
    .workplane(offset=18)
    .rect(62, 10)
    .loft()
)

# Second floor / dormer addition on top front
dormer_body = (
    cq.Workplane("XY")
    .center(0, -8)
    .rect(50, 30)
    .extrude(38)
)

dormer_roof = (
    cq.Workplane("XY")
    .center(0, -8)
    .workplane(offset=38)
    .rect(52, 32)
    .workplane(offset=12)
    .rect(40, 6)
    .loft()
)

# Side wing
side_wing = (
    cq.Workplane("XY")
    .center(45, -5)
    .rect(25, 35)
    .extrude(20)
)

side_wing_roof = (
    cq.Workplane("XY")
    .center(45, -5)
    .workplane(offset=20)
    .rect(27, 37)
    .workplane(offset=10)
    .rect(15, 5)
    .loft()
)

# Tower / silo structure (octagonal)
tower_base = (
    cq.Workplane("XY")
    .center(-55, 5)
    .polygon(8, 22)
    .extrude(25)
)

# Tower roof (conical approximation with octagonal loft)
tower_roof = (
    cq.Workplane("XY")
    .center(-55, 5)
    .workplane(offset=25)
    .polygon(8, 24)
    .workplane(offset=10)
    .polygon(8, 2)
    .loft()
)

# Tower upper section
tower_upper = (
    cq.Workplane("XY")
    .center(-55, 5)
    .workplane(offset=18)
    .polygon(8, 20)
    .extrude(7)
)

# Chimney 1
chimney1 = (
    cq.Workplane("XY")
    .center(5, 0)
    .rect(5, 5)
    .extrude(52)
)

# Chimney 2
chimney2 = (
    cq.Workplane("XY")
    .center(-10, 5)
    .rect(4, 4)
    .extrude(50)
)

# Combine all parts
result = (
    main_body
    .union(main_roof)
    .union(dormer_body)
    .union(dormer_roof)
    .union(side_wing)
    .union(side_wing_roof)
    .union(tower_base)
    .union(tower_upper)
    .union(tower_roof)
    .union(chimney1)
    .union(chimney2)
)