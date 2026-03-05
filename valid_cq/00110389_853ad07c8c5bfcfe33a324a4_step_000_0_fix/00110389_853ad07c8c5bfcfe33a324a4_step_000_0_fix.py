import cadquery as cq

# Create the main U shape with a sweep
path = cq.Workplane("XZ").moveTo(0, 30).threePointArc((15, 45), (0, 60))
section = cq.Workplane("YZ").circle(5)
u_shape = section.sweep(path)

# Create ribbed cylinder
ribbed_cylinder = cq.Workplane("XY").circle(5).extrude(30).faces(">Z").circle(6).extrude(0.5)
for i in range(9):
    ribbed_cylinder = ribbed_cylinder.faces(">Z").circle(6).extrude(0.5)

# Union the shapes
result = u_shape.union(ribbed_cylinder)

result