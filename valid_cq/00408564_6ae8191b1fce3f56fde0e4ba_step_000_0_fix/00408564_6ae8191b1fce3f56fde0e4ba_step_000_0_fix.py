import cadquery as cq

# Define the base plate
base_plate = cq.Workplane("XY").rect(100, 100).extrude(10)

# Define the cutout cylinder
cutout_cylinder = (
    cq.Workplane("XY", origin=(0, 0, 10))
    .circle(30)
    .extrude(-10)
)

# Create a tapered cup
cup = (
    cq.Workplane("XY", origin=(0, 0, 10))
    .circle(25)
    .workplane(offset=50)
    .circle(20)
    .loft()
)

# Create arm
arm = (
    cq.Workplane("XY", origin=(0, 0, 10))
    .rect(150, 10)
    .extrude(5)
)

# Create smaller arm
small_arm = (
    cq.Workplane("XY", origin=(50, 0, 10))
    .rect(50, 5)
    .extrude(5)
)

# Assemble the model
result = (
    base_plate
    .union(cup)
    .cut(cutout_cylinder)
    .union(arm)
    .union(small_arm)
)