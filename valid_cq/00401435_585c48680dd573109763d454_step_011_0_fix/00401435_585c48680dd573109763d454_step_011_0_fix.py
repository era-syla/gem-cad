import cadquery as cq

# Start with a base rectangle
result = cq.Workplane("XY").rect(100, 200).extrude(10)

# Cut operations to shape the part
result = result.faces(">Z").workplane().rect(80, 180).cutBlind(-5)
result = result.faces("<Z").workplane().rect(50, 160).extrude(10)

# Add fillets to the edges
result = result.edges("|Z").fillet(2)

# Make additional cuts for detail
result = result.faces(">Z").workplane(offset=-3).rect(40, 120).cutBlind(-2)
result = result.faces(">Z[-2]").workplane().rect(30, 100).extrude(2)

# Additional side cuts
result = result.faces(">X").workplane().rect(5, 50, centered=(True, False)).cutBlind(-90)
result = result.faces("<X").workplane().rect(5, 50, centered=(True, False)).cutBlind(-90)