import cadquery as cq

rod = (
    cq.Workplane("XY")
    .circle(1)
    .extrude(50)
)

result = (
    rod
    .union(rod.translate((2.5, 0, 0)))
    .union(rod.translate((5, 0, 0)))
    .union(rod.translate((7.5, 0, 0)))
    .union(rod.translate((10, 0, 0)))
    .union(rod.translate((12.5, 0, 0)))
)