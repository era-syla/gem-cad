import cadquery as cq

# Parameters
width = 80
height = 150
thickness = 5
arc_depth = 10
arc_radius = 400
foot_spacing = 30
foot_length = 20
foot_height = 10
center_foot_width = 10

# Main plate
plate = (
    cq.Workplane("XY")
    .rect(width, height)
    .extrude(thickness)
)

# Cut a shallow concave arc at the bottom center of the plate
arc_cutter = (
    cq.Workplane("XY")
    .transformed(offset=(0, -(arc_radius - arc_depth), thickness/2))
    .circle(arc_radius)
    .extrude(thickness * 2)
)
plate = plate.cut(arc_cutter)

# Left foot
foot1 = (
    cq.Workplane("XY")
    .transformed(offset=(-foot_spacing, -foot_height/2, thickness/2))
    .box(foot_length, foot_height, thickness)
)

# Right foot
foot2 = (
    cq.Workplane("XY")
    .transformed(offset=(foot_spacing, -foot_height/2, thickness/2))
    .box(foot_length, foot_height, thickness)
)

# Center foot (fits into the concave arc)
cfoot = (
    cq.Workplane("XY")
    .transformed(offset=(0, -foot_height/2, thickness/2))
    .box(center_foot_width, foot_height, thickness)
)

# Combine everything
result = plate.union(foot1).union(foot2).union(cfoot)