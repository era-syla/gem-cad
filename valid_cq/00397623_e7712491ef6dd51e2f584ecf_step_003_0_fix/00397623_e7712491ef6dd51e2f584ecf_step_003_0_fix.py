import cadquery as cq

# Create the main base
base = cq.Workplane("XY").box(60, 20, 10)

# Create the central cylinder
cylinder = cq.Workplane("XY").circle(10).extrude(10)

# Combine base and cylinder
result = base.union(cylinder)

# Cut the central hole in the cylinder
result = result.faces(">Z").workplane().circle(5).cutThruAll()

# Add holes to the base
result = result.faces(">Z").workplane().pushPoints([(-20, 0), (20, 0)]).hole(3)

# Add holes to the top
result = result.faces(">Z").workplane(centerOption='CenterOfBoundBox').pushPoints([(10, 0), (-10, 0)]).hole(2)

result