import cadquery as cq

# Parameters for a standard 2020 extrusion profile
length = 600.0
width = 20.0
opening_w = 6.2
opening_d = 1.8
inner_w = 12.0
inner_d = 4.2
hole_r = 2.5
chamfer_size = 1.0

# Create the base block
base = cq.Workplane("XY").box(width, width, length)

# Add chamfers to the outer edges along the Z axis
result = base.edges("|Z").chamfer(chamfer_size)

# Create a workplane on the top face
wp = result.faces(">Z").workplane()

# Cut central hole
result = wp.circle(hole_r).cutBlind(-length)

# Cut top and bottom slot openings
result = (
    result.faces(">Z").workplane()
    .pushPoints([
        (0, width/2 - opening_d/2), 
        (0, -width/2 + opening_d/2)
    ])
    .rect(opening_w, opening_d)
    .cutBlind(-length)
)

# Cut left and right slot openings
result = (
    result.faces(">Z").workplane()
    .pushPoints([
        (width/2 - opening_d/2, 0), 
        (-width/2 + opening_d/2, 0)
    ])
    .rect(opening_d, opening_w)
    .cutBlind(-length)
)

# Cut top and bottom inner slot profiles
result = (
    result.faces(">Z").workplane()
    .pushPoints([
        (0, width/2 - opening_d - inner_d/2), 
        (0, -width/2 + opening_d + inner_d/2)
    ])
    .rect(inner_w, inner_d)
    .cutBlind(-length)
)

# Cut left and right inner slot profiles
result = (
    result.faces(">Z").workplane()
    .pushPoints([
        (width/2 - opening_d - inner_d/2, 0), 
        (-width/2 + opening_d + inner_d/2, 0)
    ])
    .rect(inner_d, inner_w)
    .cutBlind(-length)
)