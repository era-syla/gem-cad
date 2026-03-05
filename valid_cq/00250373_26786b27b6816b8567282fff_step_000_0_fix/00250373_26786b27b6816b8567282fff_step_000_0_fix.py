import cadquery as cq

# Create the main cylinder
main_cylinder = cq.Workplane("XY").circle(10).extrude(10)

# Create the horizontal cylinder
horizontal_cylinder = cq.Workplane("XY").circle(5).extrude(30).translate((0, 0, 5))

# Create the vertical boss
vertical_cylinder = cq.Workplane("XY").circle(5).extrude(20).translate((0, 0, 15))

# Fillet the top of the vertical boss
vertical_cylinder = vertical_cylinder.faces(">Z").edges().fillet(1)

# Combine all parts
result = main_cylinder.union(horizontal_cylinder).union(vertical_cylinder)