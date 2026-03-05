import cadquery as cq

# Base plate
result = cq.Workplane("XY").rect(60, 100).extrude(10)

# Main pocket
result = result.faces(">Z").workplane().rect(50, 90).cutBlind(-4)

# Inner rectangle shapes
result = result.faces(">Z").workplane().rect(15, 20).extrude(6)
result = result.faces(">Z").workplane().center(0, -25).rect(15, 20).extrude(6)

# Add mounting holes
result = result.faces(">Z").workplane().pushPoints([(-30, 50), (30, 50), (-30, -50), (30, -50)]).hole(6)

# Peripheral features (e.g., chamfers)
result = result.edges("|Z").chamfer(2)

result = result.edges(">Z").chamfer(1)