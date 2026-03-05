import cadquery as cq

flange_diameter = 20
flange_thickness = 3
shaft_diameter = 10
shaft_length = 60

result = (
    cq.Workplane("XY")
    .circle(flange_diameter / 2)
    .extrude(flange_thickness)
    .faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)