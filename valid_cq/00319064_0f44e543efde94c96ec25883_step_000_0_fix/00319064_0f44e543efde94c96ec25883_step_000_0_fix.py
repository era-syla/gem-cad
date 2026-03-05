import cadquery as cq

# Base of the link with holes
link = (
    cq.Workplane("XY")
    .circle(10)
    .extrude(3)
    .faces(">Z")  # Work from the top face
    .workplane()
    .circle(5)
    .cutThruAll()
    .faces(">Z")
    .workplane()
    .hole(2)
)

# Arm of the link with embossed text
arm = (
    cq.Workplane("XY")
    .rect(40, 15)
    .extrude(3)
    .edges("|Z")
    .fillet(2)
    .faces(">Z")
    .text("35mm", 6, 1)
    .translate((0, 0, 3))
)

# Combine features
result = link.union(arm.translate((0, 0, 1.5)))