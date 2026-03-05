import cadquery as cq

# Create the cylindrical base
cylinder = cq.Workplane("XY").circle(10).extrude(40)

# Create the dome on top
sphere = cq.Workplane("XY").sphere(10).translate((0, 0, 40))

# Combine the cylinder and the dome
result = cylinder.union(sphere)