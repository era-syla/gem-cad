import cadquery as cq

# Create the main U-shaped profile
u_shape = (
    cq.Workplane("XY")
    .box(30, 60, 4, centered=(True, True, False))
    .faces(">Z")
    .workplane()
    .rect(22, 50)
    .cutBlind(-4)
)

# Add the end block with a hole
end_block = (
    cq.Workplane("XY")
    .box(8, 60, 4, centered=(False, True, False))
    .translate((11, 0, 0))
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .circle(2)
    .cutBlind(-4)
)

# Combine the shapes
result = u_shape.union(end_block)