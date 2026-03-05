import cadquery as cq

bolt_length = 50
bolt_diameter = 10
head_height = 5
head_diameter = 20

bolt = cq.Workplane("XY").circle(bolt_diameter / 2).extrude(bolt_length)

bolt_head = (
    cq.Workplane("XY")
    .polygon(6, head_diameter)
    .extrude(head_height)
    .translate((0, 0, bolt_length))
)

result = bolt.union(bolt_head)