import cadquery as cq

# Create the base profile
base_profile = (
    cq.Workplane("XY")
    .rect(80, 30)
    .extrude(200)
)

# Create holes pattern
holes_pattern = (
    base_profile.faces("<Z").workplane()
    .rarray(15, 15, 3, 4)
    .circle(2)
    .cutThruAll()
)

# Create side cutouts
side_cutouts = (
    holes_pattern.faces(">X").workplane(centerOption='CenterOfBoundBox')
    .rarray(50, 50, 2, 4)
    .rect(10, 10)
    .cutThruAll()
)

# Fillet edges
final_geometry = side_cutouts.edges().fillet(2)

result = final_geometry