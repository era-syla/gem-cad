import cadquery as cq

# Create the main profile
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(20, 0)
    .lineTo(35, 40)
    .lineTo(35, 60)
    .lineTo(15, 80)
    .lineTo(0, 65)
    .close()
)

# Extrude to create thickness
result = profile.extrude(5)

# Add holes
result = (
    result.faces(">Z").workplane()
    .pushPoints([(5, 5), (30, 50), (10, 15)])
    .hole(5)
)