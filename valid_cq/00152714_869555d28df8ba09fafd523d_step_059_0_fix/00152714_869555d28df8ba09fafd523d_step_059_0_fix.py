import cadquery as cq

# Create the main workplane
result = (
    cq.Workplane("XY")
    .polygon(3, 40)
    .extrude(5)
    .edges("|Z")
    .fillet(2)
    .faces(">Z")
    .workplane()
    .hole(10)
    .workplane(offset=-5)
    .transformed(rotate=(0, 0, 120))
    .workplane(offset=5)
    .hole(10)
)

result = result.faces(">Z").workplane().center(-20, 0).hole(10).center(40, 0).hole(10)