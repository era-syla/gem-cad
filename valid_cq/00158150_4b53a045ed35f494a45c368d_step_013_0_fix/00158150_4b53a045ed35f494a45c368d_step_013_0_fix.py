import cadquery as cq

result = (
    cq.Workplane("XY")
    # Base plate
    .rect(100, 40).extrude(4)
    # Circular ring boss
    .faces(">Z").workplane(centerOption="CenterOfBoundBox").center(25, 0) \
        .circle(20).circle(15).extrude(6)
    # Countersunk hole in the boss
    .faces(">Z").workplane().center(25, 0).cskHole(3, 6, 90)
    # Raised label pad
    .faces(">Z").workplane().center(-25, 0).rect(20, 5).extrude(1)
    # Alignment pins under the boss
    .faces("<Z").workplane().pushPoints([(30, 10), (30, -10)]).circle(2.5).extrude(-8)
    # Mounting legs at the front
    .faces("<Z").workplane().pushPoints([(-45, 10), (-45, -10)]).rect(5, 5).extrude(-5)
    # Fillet all vertical edges
    .edges("|Z").fillet(1)
)