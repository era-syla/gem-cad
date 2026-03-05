import cadquery as cq

length = 160.0
width = 100.0
thickness = 3.0
tab_depth = 15.0
tab_width = 30.0
corner_offset = 7.5
hole_dia_large = 5.0
hole_dia_small = 3.2

outline = [
    (-width/2, -length/2 + tab_depth),
    (-tab_width/2, -length/2 + tab_depth),
    (-tab_width/2, -length/2),
    ( tab_width/2, -length/2),
    ( tab_width/2, -length/2 + tab_depth),
    ( width/2, -length/2 + tab_depth),
    ( width/2,  length/2 - tab_depth),
    ( tab_width/2,  length/2 - tab_depth),
    ( tab_width/2,  length/2),
    (-tab_width/2,  length/2),
    (-tab_width/2,  length/2 - tab_depth),
    (-width/2,     length/2 - tab_depth),
]

big_holes = [
    (-width/2 + corner_offset, -length/2 + corner_offset),
    ( width/2 - corner_offset, -length/2 + corner_offset),
    ( width/2 - corner_offset,  length/2 - corner_offset),
    (-width/2 + corner_offset,  length/2 - corner_offset),
]

small_holes = [
    (0.0,   0.0),
    (-35.0,  60.0),
    ( 35.0,  60.0),
    (-35.0, -60.0),
    ( 35.0, -60.0),
    (-25.0,   0.0),
    ( 25.0,   0.0),
]

result = (
    cq.Workplane("XY")
      .polyline(outline)
      .close()
      .extrude(thickness)
)

for pt in big_holes:
    result = result.faces(">Z").workplane().pushPoints([pt]).hole(hole_dia_large)

for pt in small_holes:
    result = result.faces(">Z").workplane().pushPoints([pt]).hole(hole_dia_small)