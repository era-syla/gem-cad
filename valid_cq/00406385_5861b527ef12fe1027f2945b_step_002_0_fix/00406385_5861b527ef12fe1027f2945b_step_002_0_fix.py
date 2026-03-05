import cadquery as cq

# Create the wing shape
wing = cq.Workplane("XY").spline([(0, 0), (2, 0.5), (5, 0.7), (9, 0.2), (10, 0)]).close().extrude(0.2)

# Create the vertical stabilizer
stabilizer = (cq.Workplane("YZ")
              .polyline([(0, 0), (0.5, 0.2), (0.5, 1), (0, 1.5)])
              .close().extrude(0.1))

# Position the stabilizer on top of the wing
stabilizer = stabilizer.translate((8, 0, 0.2))

# Combine the parts into one object
result = wing.union(stabilizer)