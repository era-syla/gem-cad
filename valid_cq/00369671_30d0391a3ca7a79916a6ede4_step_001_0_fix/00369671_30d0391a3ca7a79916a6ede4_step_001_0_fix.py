import cadquery as cq

# Create the cylinder part
cylinder = cq.Workplane("XY").circle(5).extrude(30)

# Create the rectangular block
block = cq.Workplane("XY").box(20, 20, 10)

# Combine the cylinder and block
combined = block.union(cylinder)

# Create the arc part
arc = (cq.Workplane("XY")
       .center(10, 0)
       .circle(10)
       .extrude(10)
       .cut(cq.Workplane("XY").center(10, 0).circle(5).extrude(10))
     )

# Combine arc with the existing part
result = combined.union(arc)

# Drill the hole
result = result.faces(">Z").workplane(centerOption="CenterOfMass").hole(5, 20)