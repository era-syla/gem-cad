import cadquery as cq

length = 200.0
width = 10.0
height = 5.0
hole_radius = 0.75
hole_spacing = 10.0

profile = cq.Workplane("XY").box(length, width, height)

holes = (
    profile.faces(">Z")
    .workplane()
    .rarray(hole_spacing, hole_spacing, 20, 1)
    .circle(hole_radius)
    .cutThruAll()
)

bracket = (
    holes.faces(">X[1]").workplane(offset=5)
    .rect(width, height)
    .extrude(5)
)

result = bracket.edges("|Z").fillet(1)