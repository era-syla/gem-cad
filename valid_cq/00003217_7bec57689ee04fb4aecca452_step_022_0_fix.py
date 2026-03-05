import cadquery as cq

# Wheel/roller with grooves on outer surface and recessed face
outer_radius = 40
inner_radius = 8
width = 30

# Main cylinder body
result = (
    cq.Workplane("YZ")
    .circle(outer_radius)
    .extrude(width)
)

# Add groove near front edge
result = (
    result
    .faces(">X")
    .workplane()
    .circle(outer_radius + 1)
    .circle(outer_radius - 3)
    .cutBlind(-3)
)

# Add groove near back edge
result = (
    result
    .faces("<X")
    .workplane()
    .circle(outer_radius + 1)
    .circle(outer_radius - 3)
    .cutBlind(-3)
)

# Create the recessed face on the front
result = (
    result
    .faces(">X")
    .workplane()
    .circle(outer_radius - 5)
    .cutBlind(-4)
)

# Create the recessed face on the back
result = (
    result
    .faces("<X")
    .workplane()
    .circle(outer_radius - 5)
    .cutBlind(-4)
)

# Add inner hub recess on front face
result = (
    result
    .faces(">X")
    .workplane()
    .circle(15)
    .cutBlind(-3)
)

# Central bore through entire wheel
result = (
    result
    .faces(">X")
    .workplane()
    .circle(inner_radius)
    .cutThruAll()
)

# Add outer surface grooves (two rings near edges)
# Front groove on outer surface
result = (
    result
    .faces(">X")
    .workplane(offset=-4)
    .circle(outer_radius + 0.1)
    .circle(outer_radius - 2)
    .cutBlind(-2)
)

# Back groove on outer surface
result = (
    result
    .faces("<X")
    .workplane(offset=-4)
    .circle(outer_radius + 0.1)
    .circle(outer_radius - 2)
    .cutBlind(-2)
)