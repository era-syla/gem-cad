import cadquery as cq

# Create the horizontal arm
horizontal_arm = cq.Workplane("XY").box(50, 10, 10)

# Create the vertical arm
vertical_arm = cq.Workplane("YZ").box(50, 10, 10).translate((0, 25, 0))

# Create the joining cylinder
cylinder = cq.Workplane("XY").circle(10).extrude(10).translate((5, 5, 5))

# Create the rectangular cutout
cutout = cq.Workplane("XY").box(10, 2, 2).translate((25, 2, 1))

# Assemble parts
result = horizontal_arm.union(vertical_arm).union(cylinder).cut(cutout)