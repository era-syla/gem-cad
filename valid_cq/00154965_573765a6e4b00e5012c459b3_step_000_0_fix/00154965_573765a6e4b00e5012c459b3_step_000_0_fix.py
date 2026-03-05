import cadquery as cq

# Base
base = cq.Workplane("XY").circle(30).extrude(5)

# Support Arm
support_arm = (cq.Workplane("XY", origin=(0, 0, 5))
               .rect(10, 40)
               .extrude(60)
               .faces(">Y")
               .shell(3))

# Head
head = (cq.Workplane("XY", origin=(0, 0, 65))
       .circle(15)
       .extrude(10)
       .faces(">Z")
       .hole(8))

# Screw
screw = (cq.Workplane("XZ", origin=(0, 0, 65))
        .circle(4)
        .extrude(40))

# Combine Parts
result = base.union(support_arm).union(head).union(screw)