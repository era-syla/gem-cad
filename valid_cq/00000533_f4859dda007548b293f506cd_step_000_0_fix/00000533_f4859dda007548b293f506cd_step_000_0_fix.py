import cadquery as cq
import math

# Base
base = (
    cq.Workplane("XY")
    .circle(40)
    .extrude(10)
    .faces(">Z")
    .fillet(2)
)

# First arm
arm1 = (
    cq.Workplane("XY")
    .box(4, 4, 60, centered=(True, True, False))
    .edges("|Z")
    .fillet(1)
    .translate((0, 0, 10))
    .rotate((0, 0, 10), (0, 1, 0), 45)
)

# Compute joint position for second arm
angle1 = 45
x1 = 60 * math.sin(math.radians(angle1))
z1 = 10 + 60 * math.cos(math.radians(angle1))

# Second arm
arm2 = (
    cq.Workplane("XY")
    .box(4, 4, 60, centered=(True, True, False))
    .edges("|Z")
    .fillet(1)
    .translate((x1, 0, z1))
    .rotate((x1, 0, z1), (0, 1, 0), -90)
)

# Lamp head (truncated cone)
head = (
    cq.Workplane("XY")
    .workplane(offset=0).circle(15)
    .workplane(offset=20).circle(5)
    .loft()
    .rotate((0, 0, 0), (1, 0, 0), 180)
    .translate((x1 + 30, 0, z1))
)

# Combine all parts
result = base.union(arm1.val()).union(arm2.val()).union(head.val())