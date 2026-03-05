import cadquery as cq

# Create the main body
main_body = (
    cq.Workplane("XY")
    .rect(40, 20)
    .extrude(3)
)

# Create the rounded cut-outs
cutout = (
    cq.Workplane("XY")
    .rarray(30, 10, 2, 1)
    .slot2D(10, 3)
    .extrude(3)
)

# Create the inner cut
inner_cut = (
    cq.Workplane("XY")
    .moveTo(0, -10)
    .rect(10, 10)
    .extrude(3)
)

# Create the bottom tab
bottom_tab = (
    cq.Workplane("XY")
    .moveTo(0, -13)
    .rect(10, 3)
    .extrude(3)
)

# Subtract the cutouts and the inner section
result = main_body.cut(cutout).cut(inner_cut).union(bottom_tab)