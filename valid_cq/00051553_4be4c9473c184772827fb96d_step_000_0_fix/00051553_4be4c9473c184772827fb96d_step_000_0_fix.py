import cadquery as cq

# Base shape
base = (
    cq.Workplane("XY")
    .moveTo(-15, 0)
    .lineTo(-20, 5)
    .lineTo(-15, 20)
    .lineTo(0, 10)
    .lineTo(15, 20)
    .lineTo(20, 5)
    .lineTo(15, 0)
    .close()
    .extrude(5)
)

# Adding the head
head = (
    cq.Workplane("XY")
    .moveTo(0, 10)
    .circle(5)
    .extrude(5)
)

# Combine base and head
model = base.union(head)

# Small hole in head
result = model.faces(">Z").workplane().moveTo(0, 10).circle(2).cutThruAll()