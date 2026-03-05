import cadquery as cq

# Parameters
length = 50
clear_width = 20
side_thickness = 6
base_thickness = 6
wall_height = 30
hole_dia = 8

# Base plate
base = (
    cq.Workplane("XY")
    .rect(length, clear_width + 2 * side_thickness)
    .extrude(base_thickness)
)

# Side wall 2D profile in X-Z plane
side_outline = [
    (-length/2, base_thickness),
    ( length/2, base_thickness),
    ( length/2, wall_height),
    (-length/2, wall_height),
]

# Right side wall
right_wall = (
    cq.Workplane("XZ")
    .polyline(side_outline)
    .close()
    .extrude(side_thickness)
    .translate((0, (clear_width/2 + side_thickness/2), 0))
    .faces(">Y")
    .workplane()
    .hole(hole_dia, depth=side_thickness)
)

# Left side wall
left_wall = (
    cq.Workplane("XZ")
    .polyline(side_outline)
    .close()
    .extrude(side_thickness)
    .translate((0, -(clear_width/2 + side_thickness/2), 0))
    .faces("<Y")
    .workplane()
    .hole(hole_dia, depth=side_thickness)
)

# Assemble final result
result = base.union(right_wall).union(left_wall)