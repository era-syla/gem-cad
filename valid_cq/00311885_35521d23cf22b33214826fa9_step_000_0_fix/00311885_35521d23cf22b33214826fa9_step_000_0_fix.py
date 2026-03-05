import cadquery as cq

# Main cylinder
cylinder = cq.Workplane("XY").circle(10).extrude(40)

# Caps
cap1 = cq.Workplane("XY").circle(11).extrude(1)
cap2 = cap1.translate((0, 0, 40))

# Small side cylinder
side_cylinder = cq.Workplane("XZ").circle(2).extrude(5).translate((-10, 0, 20))

# Indents on the end face
indent_circle1 = cq.Workplane("XY").circle(3).extrude(-1)
indent_circle2 = cq.Workplane("XY").circle(1.5).extrude(-0.5).translate((0, 0, -0.5))

result = cylinder.union(cap1).union(cap2).union(side_cylinder).union(indent_circle1).union(indent_circle2)