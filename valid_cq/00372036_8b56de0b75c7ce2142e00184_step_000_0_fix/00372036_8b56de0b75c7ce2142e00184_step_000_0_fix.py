import cadquery as cq

# Base shape
result = (
    cq.Workplane("XY")
    .circle(12/2)
    .extrude(5)
)

# Extended body
result = (
    result.faces(">Z")
    .workplane()
    .center(6, 0)
    .rect(30, 15)
    .extrude(5)
)

# Holes in the extension
for y in [-5, 0, 5]:
    result = (
        result.faces(">Z")
        .workplane()
        .center(15, y)
        .hole(3)
    )

# Hole in the circular part
result = (
    result.faces(">Z")
    .workplane()
    .center(-6, 0)
    .hole(6)
)