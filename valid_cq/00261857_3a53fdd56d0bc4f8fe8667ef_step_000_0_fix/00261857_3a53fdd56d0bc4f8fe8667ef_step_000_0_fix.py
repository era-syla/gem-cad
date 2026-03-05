import cadquery as cq

# Create the main body of the bottle
body = (cq.Workplane("XY")
        .circle(25)
        .extrude(60))

# Create the neck
neck = (cq.Workplane("XY")
        .circle(10)
        .extrude(15)
        .translate((0, 0, 60)))

# Create the top of the bottle with a blend
top = (cq.Workplane("XY")
       .circle(25)
       .workplane(offset=10)
       .circle(10)
       .loft()
       .translate((0, 0, 50)))

# Combine all parts
result = body.union(neck).union(top)