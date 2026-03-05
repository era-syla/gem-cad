import cadquery as cq

# Create the base shape
base = cq.Workplane("XY").box(20, 50, 10)

# Create the cutout on the top part
cutout = cq.Workplane("XY").box(10, 20, 5).translate((5, 15, 7.5))

# Subtract the cutout from the base
result = base.cut(cutout)

# Create holes
result = result.faces(">Z").workplane().hole(5)
result = result.faces("<Z").workplane().hole(5)

# The resulting solid
result