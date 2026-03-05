import cadquery as cq

# Create the base shape
base = (
    cq.Workplane("XY")
    .rect(20, 30)
    .extrude(40)
)

# Create the round head shape
head = (
    cq.Workplane("XY", origin=(0, 0, 40))
    .circle(15)
    .extrude(10)
)

# Combine the base and head
combined = base.union(head)

# Add the cut-out circle
cutout = (
    cq.Workplane("XY", origin=(0, 0, 45))
    .circle(5)
    .extrude(10)
)

# Subtract the cut-out from the head
result = combined.cut(cutout)