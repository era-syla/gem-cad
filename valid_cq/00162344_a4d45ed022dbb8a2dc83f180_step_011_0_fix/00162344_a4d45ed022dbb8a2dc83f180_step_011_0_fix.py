import cadquery as cq

# Main cylinder
result = cq.Workplane("XY").circle(10).extrude(100)

# Outer recess on top face
result = result.faces(">Z").workplane().circle(9).cutBlind(2)

# Inner shallow dish
result = result.faces(">Z").workplane().circle(4).cutBlind(1)

# Small central hole
result = result.faces(">Z").workplane().hole(1)