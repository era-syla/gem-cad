import cadquery as cq

# Create the horizontal bar
bar = cq.Workplane("XY").box(100, 10, 10)

# Create the smaller vertical piece
vertical_piece = cq.Workplane("XY").box(10, 10, 10).translate((-45, 0, -5))

# Combine the bar and the vertical piece
base = bar.union(vertical_piece)

# Create a series of holes along the bar
holes = base.faces(">Z").workplane().rarray(10, 1, 10, 1).hole(3)

# Resulting part
result = holes