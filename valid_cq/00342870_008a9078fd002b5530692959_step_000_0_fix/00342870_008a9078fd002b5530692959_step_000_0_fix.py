import cadquery as cq
import math

# Parameters
th = 4               # thickness of parts
base_len = 30
base_w = 20
pivot1 = 8           # first hinge x-position
arm1_len = 40
arm1_w = 6
pivot2 = pivot1 + arm1_len
arm2_len = 50
arm2_w = 6
angle2 = -60         # degrees

# Base block
base = cq.Workplane("XY").box(base_len, base_w, th)

# First hinge pin
pin1 = cq.Workplane("XY").transformed(offset=(pivot1, 0, th)).circle(2).extrude(2*th)

# First arm
arm1 = (
    cq.Workplane("XY")
    .transformed(offset=(pivot1 + arm1_len/2, 0, th/2))
    .rect(arm1_len, arm1_w)
    .extrude(th)
)

# Second hinge pin
pin2 = cq.Workplane("XY").transformed(offset=(pivot2, 0, th)).circle(2).extrude(2*th)

# Second arm, rotated about the second hinge
arm2 = (
    cq.Workplane("XY")
    .transformed(offset=(pivot2 + arm2_len/2, 0, th/2))
    .rect(arm2_len, arm2_w)
    .extrude(th)
    .rotate((pivot2, 0, 0), (pivot2, 0, 1), angle2)
)

# Combine all parts
result = base.union(pin1).union(arm1).union(pin2).union(arm2)