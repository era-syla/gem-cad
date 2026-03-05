import cadquery as cq

# Parameters
R_main = 30.0
H_main = 40.0
R_boss = 12.0
H_boss = 15.0
R_cut = 14.0

# Base body
main_cyl = cq.Workplane("XY").circle(R_main).extrude(H_main)

# Central boss
result = (
    main_cyl.faces(">Z").workplane()
    .circle(R_boss).extrude(H_boss)
)

# Optional: Add a slight chamfer to the boss for aesthetics
result = result.edges(">Z").chamfer(0.5)

# 3 Large circular cutouts on the perimeter
result = (
    result.faces("<Z").workplane()
    .pushPoints([(0, R_main), (-R_main, 0), (0, -R_main)])
    .circle(R_cut).cutBlind(H_main)
)

# 4th quadrant: Complex flexure/labyrinth cutout
# Create a 2D profile and extrude it
e_cut = (
    cq.Workplane("XY")
    .moveTo(12, 10)
    .lineTo(35, 10)
    .lineTo(35, 6)
    .lineTo(16, 6)
    .lineTo(16, 2)
    .lineTo(35, 2)
    .lineTo(35, -2)
    .lineTo(16, -2)
    .lineTo(16, -6)
    .lineTo(35, -6)
    .lineTo(35, -10)
    .lineTo(12, -10)
    .close()
    .extrude(H_main)
)

# Fillet the vertical edges to create the smooth organic flexure shape
e_cut = e_cut.edges("|Z").fillet(1.8)

# Subtract the complex cutout from the main body
result = result.cut(e_cut)