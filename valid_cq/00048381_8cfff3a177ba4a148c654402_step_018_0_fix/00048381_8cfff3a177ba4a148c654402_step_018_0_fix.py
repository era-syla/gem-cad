import cadquery as cq

# Base block
base = cq.Workplane("XY").box(90, 20, 10)

# Left and right supports
left_support = cq.Workplane("XY").box(20, 20, 20).translate((-35, 0, 10))
right_support = cq.Workplane("XY").box(20, 20, 20).translate((35, 0, 10))

# Combine base and supports
result = base.union(left_support).union(right_support)

# Hole in left support
result = result.faces(">X").workplane().hole(10)

# Hole in right support
result = result.faces("<X").workplane().hole(10)

# Top horizontal bar
top_bar = cq.Workplane("XY").box(60, 5, 5).translate((0, 0, 20))

# Combine with top bar
result = result.union(top_bar)

# Central cutout
result = result.faces(">Z").workplane(centerOption="CenterOfBoundBox").rect(10, 30).cutThruAll()

# Vertical cylinder through base
result = result.faces("<Z").workplane(centerOption="CenterOfBoundBox").circle(3).cutThruAll()
