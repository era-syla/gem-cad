import cadquery as cq

# Geometric parameters
diameter = 12.0
length = 40.0
chamfer_size = 1.5

# Create the main cylinder
# 1. Start a workplane on the XY plane
# 2. Draw a circle representing the diameter
# 3. Extrude to create the cylindrical solid
result = cq.Workplane("XY").circle(diameter / 2.0).extrude(length)

# Apply chamfers to the top and bottom edges
# 1. Select the faces at the maximum and minimum Z height (>Z or <Z)
# 2. Select the edges associated with those faces
# 3. Apply the chamfer
result = result.faces(">Z or <Z").edges().chamfer(chamfer_size)