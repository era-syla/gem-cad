import cadquery as cq

# Parameters
length = 80
width = 40
height = 10
cavity_dia = 30
cavity_depth = 5
boss_dia = 10
boss_height = 3
fillet_radius = 2

result = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(height)
    .edges("|Z")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .circle(cavity_dia / 2)
    .cutBlind(cavity_depth)
    .faces(">Z")
    .workplane(offset=-cavity_depth)
    .circle(boss_dia / 2)
    .extrude(boss_height)
)