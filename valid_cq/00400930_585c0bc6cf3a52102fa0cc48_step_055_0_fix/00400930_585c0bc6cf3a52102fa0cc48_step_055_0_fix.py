import cadquery as cq

# Create the base piece
base = (cq.Workplane("XY")
        .box(60, 10, 3)
        .faces(">Z")
        .workplane()
        .circle(5)
        .cutThruAll())

# Create the vertical pieces
vertical1 = (cq.Workplane("XY")
             .box(10, 10, 20)
             .translate((-25, 0, 10)))

vertical2 = (cq.Workplane("XY")
             .box(10, 10, 40)
             .translate((25, 0, 20)))

# Create the horizontal piece
horizontal = (cq.Workplane("XY")
              .box(60, 10, 3)
              .translate((0, 0, 40)))

# Combine all parts into one result
result = base.union(vertical1).union(vertical2).union(horizontal)