import cadquery as cq

# Create the main cylindrical body
cylinder = cq.Workplane("XY").circle(10).extrude(60)

# Create the larger disc on one end
disc = cq.Workplane("XY").circle(15).extrude(5)

# Combine the two parts
result = cylinder.union(disc)

# Create a hole through the main cylinder
result = result.faces(">Z").workplane().circle(2).cutThruAll()