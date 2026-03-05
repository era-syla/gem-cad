import cadquery as cq

# Create the vertical cylinder
vertical_cylinder = cq.Workplane("XY").circle(1).extrude(50)

# Create the first horizontal cylinder
horizontal_cylinder1 = cq.Workplane("XY").circle(1).extrude(20).rotate((0, 0, 0), (0, 1, 0), 90).translate((0, -20, 0))

# Create the second horizontal cylinder
horizontal_cylinder2 = cq.Workplane("XY").circle(1).extrude(18).rotate((0, 0, 0), (0, 1, 0), 90).translate((0, -18, 0))

# Combine the cylinders
result = vertical_cylinder.union(horizontal_cylinder1).union(horizontal_cylinder2)