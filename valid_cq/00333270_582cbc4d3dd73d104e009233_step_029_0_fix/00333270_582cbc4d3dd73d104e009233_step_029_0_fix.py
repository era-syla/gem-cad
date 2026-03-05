import cadquery as cq

# Base plate
result = cq.Workplane("XY").box(60, 30, 5)

# Center hole
result = result.faces(">Z").workplane().circle(5).cutThruAll()

# Side holes
result = result.faces(">Z").workplane().center(-20, 0).circle(3).cutThruAll()
result = result.faces(">Z").workplane().center(40, 0).circle(3).cutThruAll()

# Center rectangle feature
result = result.faces(">Z").workplane().center(0, 0).rect(10, 15).extrude(2)

# Two small cubes on each side
result = result.faces(">Z").workplane().center(-20, 10).rect(5, 5).extrude(2)
result = result.faces(">Z").workplane().center(20, 10).rect(5, 5).extrude(2)

# Fillet on edges of the base plate
result = result.edges("|Z").fillet(1)