import cadquery as cq

# Create the main elongated plate with one rounded end
plate = (
    cq.Workplane("XY")
    .moveTo(-95, -10)
    .lineTo(95, -10)
    .threePointArc((105, 0), (95, 10))
    .lineTo(-95, 10)
    .close()
    .extrude(5)
)

# Add a bracket block on top with two through‐holes
bracket = (
    plate.faces(">Z")
    .workplane()
    .rect(20, 30)
    .extrude(5)
    .faces(">Z")
    .workplane()
    .pushPoints([(-5, 0), (5, 0)])
    .hole(4)
)

# Combine plate and bracket into one solid
result = plate.union(bracket)