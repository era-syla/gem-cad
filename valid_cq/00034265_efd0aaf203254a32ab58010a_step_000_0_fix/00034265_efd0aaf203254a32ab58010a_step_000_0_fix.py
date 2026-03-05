import cadquery as cq

# Base
result = cq.Workplane("XY").box(80, 10, 2)

# End cylinders
result = result.faces(">Z").workplane().center(-35, 0).circle(5).extrude(2)
result = result.faces(">Z").workplane().center(70, 0).circle(5).extrude(2)

# Center cylinder
result = result.faces(">Z").workplane().center(-35, 0).circle(2).extrude(10)

# Fillet edges of the base
result = result.edges("|Z").fillet(1)

# Holes
result = result.faces(">Z").workplane().center(-35, 0).circle(1).cutThruAll()
result = result.faces(">Z").workplane().center(70, 0).circle(1).cutThruAll()
result = result.faces(">Z").workplane().center(0, 0).circle(0.7).cutThruAll()
