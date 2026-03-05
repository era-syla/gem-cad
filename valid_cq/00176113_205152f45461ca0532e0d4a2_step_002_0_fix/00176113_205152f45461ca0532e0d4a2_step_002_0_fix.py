import cadquery as cq

# Base
result = cq.Workplane("XY").box(20, 5, 100)

# Hole at one end
result = result.faces(">Z").workplane().circle(5).cutThruAll()

# Hole at the other end
result = result.faces("<Z").workplane().circle(5).cutThruAll()

# Fillet the edges
result = result.edges("|Z").fillet(2)