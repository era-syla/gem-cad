import cadquery as cq

# Create a hollow rectangular profile
outer = cq.Workplane("XY").rect(10, 10).extrude(50)
inner = cq.Workplane("XY").rect(8, 8).extrude(50)
hollow_profile = outer.cut(inner)

# Create a series of holes along one side
result = hollow_profile.faces(">Y").workplane().pushPoints([(0, y) for y in range(-20, 30, 5)]).hole(1)
