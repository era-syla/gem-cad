import cadquery as cq

# Create the main cylinder
cylinder = cq.Workplane("XY").cylinder(30, 20)

# Create fins using polar array of rings
fins = (cq.Workplane("XY")
        .circle(20)
        .extrude(0.5)
        .faces(">Z")
        .workplane()
        .polarArray(0, 0, 360, 20)
        .circle(25)
        .cutBlind(2))

# Create the head on top of the cylinder
head = (cq.Workplane("XY")
        .workplane(offset=30)
        .circle(25)
        .extrude(10)
        .edges(">Z")
        .fillet(2))

# Assemble components
result = cylinder.union(fins).union(head)