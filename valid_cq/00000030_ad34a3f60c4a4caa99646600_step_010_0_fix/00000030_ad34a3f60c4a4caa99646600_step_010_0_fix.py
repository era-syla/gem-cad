import cadquery as cq

outer_radius = 20
inner_radius = 16
height = 80

result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutThruAll()
)