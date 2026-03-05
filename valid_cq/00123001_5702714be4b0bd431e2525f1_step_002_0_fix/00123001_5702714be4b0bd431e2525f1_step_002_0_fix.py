import cadquery as cq

# Create the main body of the link
body = (cq.Workplane("XY")
        .rect(5, 20)
        .extrude(5))

# Create holes at each end
hole1 = (cq.Workplane("XY")
         .moveTo(-7.5, 0)
         .circle(2.5)
         .extrude(5))

hole2 = (cq.Workplane("XY")
         .moveTo(7.5, 0)
         .circle(2.5)
         .extrude(5))

# Union the main body with the holes
result = body.union(hole1).union(hole2)