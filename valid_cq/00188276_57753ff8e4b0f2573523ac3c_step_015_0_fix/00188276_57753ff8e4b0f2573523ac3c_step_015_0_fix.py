import cadquery as cq

# Base plate with rounded edges
result = cq.Workplane("XY").box(70, 60, 15).edges("|Z").fillet(4)

# Central counterbore pocket and through hole
result = result.faces(">Z").workplane().circle(15).cutBlind(-10)
result = result.faces("<Z").workplane().circle(5).cutThruAll()

# Four corner mounting holes
for dx, dy in [(-20, -15), (-20, 15), (20, -15), (20, 15)]:
    result = result.faces(">Z").workplane().center(dx, dy).hole(5)

# Two side standoffs with through holes
for y in (15, -15):
    standoff = (
        cq.Workplane("XY")
        .workplane(offset=7.5)
        .center(35, y)
        .circle(4)
        .extrude(15)
        .faces(">Z")
        .workplane()
        .hole(4)
    )
    result = result.union(standoff)

# Front rectangular pocket
result = result.faces("<Y").workplane().rect(40, 20).cutBlind(-10)

# Boss and square boss inside front pocket
result = result.faces("<Y").workplane(offset=-10).circle(3).extrude(2)
result = result.faces("<Y").workplane(offset=-10).rect(6, 6).extrude(1)