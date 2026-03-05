import cadquery as cq

# Create the main cylinder
cylinder = cq.Workplane("XY").circle(10).extrude(50)

# Create end caps
cap1 = (cq.Workplane("XY")
        .circle(12)
        .extrude(5)
        .faces(">Z")
        .workplane()
        .rect(8, 8)
        .extrude(10)
        .faces(">Z")
        .workplane(centerOption="CenterOfMass")
        .circle(4)
        .cutBlind(-5))

cap2 = cap1.mirror("XZ").translate((0, 0, 50))

# Assemble the parts
result = cylinder.union(cap1).union(cap2)