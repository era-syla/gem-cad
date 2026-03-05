import cadquery as cq

# Create the base profile
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(10, 0)
    .threePointArc((15, 5), (10, 10))
    .lineTo(0, 10)
    .close()
)

# Extrude the profile
main_body = profile.extrude(5)

# Cut holes in the main body
holes = (
    main_body.faces(">Z").workplane()
    .pushPoints([(2.5, 2.5), (7.5, 2.5), (12.5, 7.5)])
    .hole(1)
)

# Create the vertical arm
arm_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 5)
    .lineTo(0, 15)
    .threePointArc((5, 20), (0, 25))
    .lineTo(0, 30)
    .close()
)

# Extrude the arm and combine with the main body
arm = arm_profile.extrude(2.5)
combined = holes.union(arm)

# Create the fillets
result = combined.edges("|Z").fillet(0.5)