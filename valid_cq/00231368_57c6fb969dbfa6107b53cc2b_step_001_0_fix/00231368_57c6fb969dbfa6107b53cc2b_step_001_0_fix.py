import cadquery as cq

# Define the violin body outline
body_pts = [
    (-50, 125),
    (-40, 110),
    (-25,  75),
    (-30,   0),
    (-25, -75),
    (-40,-110),
    (-50,-125),
    ( 50,-125),
    ( 40,-110),
    ( 25, -75),
    ( 30,   0),
    ( 25,  75),
    ( 40, 110),
    ( 50, 125),
]

# Create the body by extruding the outline
body = (
    cq.Workplane("XY")
    .polyline(body_pts)
    .close()
    .extrude(6)
)

# Cut simple f-holes (rectangular slots) from the top face
body = (
    body
    .faces(">Z").workplane()
    .center(-20, 10).rect(4, 40).cutBlind(-2)
    .faces(">Z").workplane()
    .center( 20, 10).rect(4, 40).cutBlind(-2)
)

# Create the neck as a rectangular prism
neck = (
    cq.Workplane("XY")
    .transformed(offset=(0, -165, 0))
    .rect(10, 80)
    .extrude(6)
)

# Create a simple scroll / pegbox as a cylinder
scroll = (
    cq.Workplane("XY")
    .transformed(offset=(0, -215, 0))
    .circle(12)
    .extrude(6)
)

# Combine all parts
result = body.union(neck).union(scroll)