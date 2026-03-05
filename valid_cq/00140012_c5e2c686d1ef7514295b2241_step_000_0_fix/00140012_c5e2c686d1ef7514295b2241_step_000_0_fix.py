import cadquery as cq

# Hexagonal base
base = cq.Workplane("XY").polygon(6, 20).extrude(10)

# Vertical tube
vertical_tube = cq.Workplane("XY").circle(5).extrude(40)

# Combine base and vertical tube
main_body = base.union(vertical_tube.translate((0, 0, 10)))

# Horizontal tube
horizontal_tube = cq.Workplane("YZ").circle(5).extrude(20)

# Translate horizontal tube and combine with main body
result = main_body.union(horizontal_tube.rotate((0, 0, 0), (0, 0, 1), 90).translate((10, 0, 25)))