import cadquery as cq

# Create the main vertical block
main_block = cq.Workplane("XY").box(10, 5, 50)

# Create the wider section on top
top_block = cq.Workplane("XY").box(20, 5, 10).translate((0, 0, 45))

# Combine the two sections
combined = main_block.union(top_block)

# Create the hole at the top
result = combined.faces(">Z").workplane(centerOption='CenterOfBoundBox').hole(5)

result