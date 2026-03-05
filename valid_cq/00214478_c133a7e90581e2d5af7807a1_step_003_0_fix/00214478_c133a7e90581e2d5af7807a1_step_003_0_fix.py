import cadquery as cq

# Main L-shaped profile
base = cq.Workplane("XY").box(80, 20, 10)

# Vertical extension
vertical = cq.Workplane("XY").box(20, 20, 70).translate((30, 0, 10))

# Combine main profile and extension
result = base.union(vertical)

# Drilling holes
hole_positions = [(40, 0, 5), (-30, 0, 5), (0, 0, 45), (30, 0, 75)]
for pos in hole_positions:
    result = result.faces(">Z").workplane(centerOption='CenterOfMass').pushPoints([pos[:2]]).hole(5)

# Fillet edges
result = result.edges("|Z").fillet(2)
result
