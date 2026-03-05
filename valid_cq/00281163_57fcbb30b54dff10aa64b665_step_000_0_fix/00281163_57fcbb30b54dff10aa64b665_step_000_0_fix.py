import cadquery as cq

width = 10
height = 50
flange_thickness = 2
web_thickness = 1

result = (
    cq.Workplane("XY")
    .box(width, flange_thickness, height)
    .faces(">Z")
    .workplane()
    .box(web_thickness, flange_thickness, height - 2 * flange_thickness)
    .translate((0, 0, -height / 2))
)