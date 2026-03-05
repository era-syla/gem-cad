import cadquery as cq

# Define main cylinder
main_cylinder = cq.Workplane("XY").circle(10).extrude(100)

# Define end cap
end_cap = cq.Workplane("XY").circle(12).extrude(5)

# Position end caps at both ends
end_cap_front = end_cap.translate((0, 0, 100))
end_cap_back = end_cap

# Define side pipe
side_pipe = cq.Workplane("XY").circle(3).extrude(20).rotate((0,0,0),(0,1,0),45).translate((0,0,50))

# Combine all parts
result = main_cylinder.union(end_cap_front).union(end_cap_back).union(side_pipe)