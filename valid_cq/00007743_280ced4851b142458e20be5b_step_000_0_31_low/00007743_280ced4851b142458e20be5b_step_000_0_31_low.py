import cadquery as cq

# Parameters
width = 60.0
height = 15.0
depth = 20.0
thickness = 5.0
central_radius = 8.0
hole_radius = 1.5
side_hole_radius = 1.5

# Base geometry
base = (
    cq.Workplane("XY")
    .box(width, depth, height)
    .edges("|Z")
    .fillet(2.0)
)

# Central cutout
central_cutout = (
    cq.Workplane("XZ")
    .workplane(offset=depth/2)
    .cylinder(depth, central_radius)
)

result = base.cut(central_cutout)

# Bottom cutout
bottom_cutout = (
    cq.Workplane("XY")
    .workplane(offset=-height/2)
    .box(width - 2 * thickness, depth + 1, height + 1)
)

result = result.cut(bottom_cutout)

# Top holes
result = (
    result.faces(">Y").workplane()
    .pushPoints([(-15, 0), (-20, 0), (15, 0), (20, 0)])
    .hole(hole_radius * 2)
)

# Side holes
result = (
    result.faces(">X").workplane()
    .pushPoints([(0, -height/4)])
    .hole(side_hole_radius * 2)
)
result = (
    result.faces("<X").workplane()
    .pushPoints([(0, -height/4)])
    .hole(side_hole_radius * 2)
)

# Fillets
result = result.edges("|Z").fillet(1.0)