import cadquery as cq

# Base cylinder
outer = (
    cq.Workplane("XY")
    .circle(10)
    .extrude(60)
)

# Inner hollow
inner = (
    cq.Workplane("XY", origin=(0, 0, 5))
    .circle(5)
    .extrude(50)
)

# Spiral cut out
spiral_section = (
    cq.Workplane("XZ")
    .moveTo(0, 5)
    .lineTo(0, 55)
    .lineTo(10, 55)
    .lineTo(10, 5)
    .close()
    .revolve(360, axisStart=(0, 0, 5), axisEnd=(0, 0, 55))
)

result = outer.cut(inner).cut(spiral_section)