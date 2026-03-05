import cadquery as cq

result = cq.Workplane("XY").box(20, 100, 5) \
    .faces(">Z").workplane().rect(15, 80).cutBlind(-2) \
    .faces(">Z").workplane().circle(7).cutBlind(-3) \
    .faces(">Z").workplane(offset=30).circle(7).cutBlind(-3) \
    .edges("|Z").fillet(1)
