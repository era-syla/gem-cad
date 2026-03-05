import cadquery as cq

bot_dia = 12
bot_h = 10
cone_top_dia = 40
cone_h = 30
flange_r = 30
flange_thk = 5
wing_len = 40
wing_wid = 12
pocket_len = 30
pocket_wid = 6
pocket_d = 3
hole_dia = 2
hole_offset = 10
top_dia = 12
top_h = 30
star_d = 12
star_h = 8

result = (
    cq.Workplane("XY")
    .circle(bot_dia/2)
    .workplane(offset=bot_h)
    .circle(cone_top_dia/2)
    .loft()
    .faces(">Z")
    .workplane()
    .circle(flange_r)
    .extrude(flange_thk)
    .faces(">Z")
    .workplane()
    .transformed(offset=(flange_r + wing_len/2, 0, 0))
    .rect(wing_len, wing_wid)
    .extrude(flange_thk)
    .faces(">Z")
    .workplane()
    .center(flange_r + wing_len/2 - pocket_len/2, 0)
    .rect(pocket_len, pocket_wid)
    .cutBlind(pocket_d)
    .faces(">Z")
    .workplane()
    .center(flange_r + hole_offset, 0)
    .hole(hole_dia)
    .faces(">Z")
    .workplane()
    .circle(top_dia/2)
    .extrude(top_h)
    .faces(">Z")
    .workplane()
    .polygon(3, star_d)
    .extrude(star_h)
)
