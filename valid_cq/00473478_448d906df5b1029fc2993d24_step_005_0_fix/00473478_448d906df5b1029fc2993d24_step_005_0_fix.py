import cadquery as cq

# Base shape
base = cq.Workplane("XY").rect(80, 20).extrude(10)

# Rear cylindrical parts
cylinders = (
    base.faces(">Z")
    .workplane()
    .center(30, 0)
    .circle(5)
    .extrude(10)
    .faces(">Z")
    .workplane()
    .circle(3)
    .cutThruAll()
    .faces(">Z")
    .workplane()
    .center(-10, 0)
    .circle(5)
    .extrude(10)
    .faces(">Z")
    .workplane()
    .circle(3)
    .cutThruAll()
)

# Vertical tab
vertical_tab = (
    base.faces(">Z")
    .workplane()
    .center(-25, 0)
    .rect(10, 10)
    .extrude(20)
)

# Hole in the base
base_hole = (
    base.faces(">Z")
    .workplane()
    .center(-10, 0)
    .circle(3)
    .cutBlind(-10)
)

# Combine all parts
result = base.union(cylinders).union(vertical_tab)