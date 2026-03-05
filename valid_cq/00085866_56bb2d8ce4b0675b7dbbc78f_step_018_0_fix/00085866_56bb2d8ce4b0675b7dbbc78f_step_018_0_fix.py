import cadquery as cq

# Parameters
base_length = 60
base_width = 10
base_height = 5
clamp_radius = 15
clamp_height = 10
hole_radius = 2

# Base rectangle
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_height)
)

# Clamp body
clamp = (
    cq.Workplane("XY")
    .circle(clamp_radius)
    .extrude(clamp_height)
)

# Union base and clamp
result = base.union(clamp)

# Creating holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-25, 0), (25, 0)])
    .hole(hole_radius * 2)
)

# Split cut in the clamp
result = (
    result.faces(">Z")
    .workplane()
    .center(0, clamp_radius)
    .rect(10, 15)
    .cutThruAll()
)