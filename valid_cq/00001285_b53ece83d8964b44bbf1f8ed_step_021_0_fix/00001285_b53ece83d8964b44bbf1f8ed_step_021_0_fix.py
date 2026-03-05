import cadquery as cq

outer_diameter = 100
inner_diameter = 50
thickness = 10

result = (
    cq.Workplane("XY")
    .circle(outer_diameter/2)
    .circle(inner_diameter/2)
    .extrude(thickness)
)