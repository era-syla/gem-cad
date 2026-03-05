import cadquery as cq

beam_width = 10
beam_height = 2
web_thickness = 2
flange_length = 30
flange_thickness = 1

web = (
    cq.Workplane("XY")
    .box(web_thickness, beam_width, beam_height)
)

flange = (
    cq.Workplane("XY")
    .workplane(offset=-beam_height/2)
    .box(flange_length, flange_thickness, beam_height)
    .translate((0, (beam_width - flange_thickness) / 2, 0))
    .edges("|Z")
    .fillet(0.2)
)

result = web.union(flange).union(flange.mirror("XZ"))