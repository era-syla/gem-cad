import cadquery as cq

# Create the main hull of the boat
hull = (cq.Workplane("XY")
        .lineTo(50, 0)
        .lineTo(100, 20)
        .lineTo(100, 60)
        .lineTo(50, 80)
        .lineTo(0, 60)
        .close()
        .extrude(20))

# Create the cabin
cabin = (cq.Workplane("XY")
         .center(25, 30)
         .rect(40, 30)
         .extrude(10))

# Create the roof of the cabin
roof = (cq.Workplane("XY")
        .center(25, 30)
        .moveTo(0, 15)
        .lineTo(20, 5)
        .lineTo(40, 15)
        .lineTo(40, 25)
        .lineTo(20, 35)
        .lineTo(0, 25)
        .close()
        .extrude(5))

# Combine the parts
result = hull.union(cabin).union(roof)