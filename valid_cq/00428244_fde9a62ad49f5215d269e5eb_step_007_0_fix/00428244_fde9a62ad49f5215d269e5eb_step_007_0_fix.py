import cadquery as cq

# Base rectangle shape
result = cq.Workplane("XY").rect(100, 50).extrude(5)

# Add multiple holes
holes = [(x, y) for x in range(-45, 50, 15) for y in range(-20, 25, 15)]
result = result.faces(">Z").workplane().pushPoints(holes).hole(2)

# Create larger central holes
larger_holes = [(x, y) for x in range(-30, 35, 15) for y in range(-15, 20, 15)]
result = result.faces(">Z").workplane().pushPoints(larger_holes).cskHole(4, 8, 82)

# Apply fillets to the edges
result = result.edges("|Z").fillet(2)