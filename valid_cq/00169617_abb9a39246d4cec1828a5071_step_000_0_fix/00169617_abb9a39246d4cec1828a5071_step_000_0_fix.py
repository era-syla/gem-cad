import cadquery as cq

# Base cylinder
base = cq.Workplane("XY").circle(20).extrude(20)

# Hollow the cylinder
hollow = base.faces(">Z").workplane().circle(17).cutBlind(-18)

# Ridges inside the hollow
for angle in range(0, 360, 60):
    ridge = (
        hollow.faces("<Z").workplane(centerOption="CenterOfBoundBox")
        .transformed(rotate=(0, 0, angle))
        .rect(5, 1)
        .extrude(18)
    )
    hollow = hollow.union(ridge)

# Side support extensions
extension = (
    cq.Workplane("XY").center(25, 0)
    .rect(5, 15)
    .extrude(20)
    .faces(">X")
    .workplane(centerOption="CenterOfBoundBox")
    .circle(2)
    .cutThruAll()
)
extensions = extension.mirror("YZ")

# Combine everything
result = hollow.union(extensions)