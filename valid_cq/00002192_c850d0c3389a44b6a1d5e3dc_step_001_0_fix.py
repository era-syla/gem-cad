import cadquery as cq

# Main body - roughly a rounded rectangular block
body = (
    cq.Workplane("XY")
    .box(40, 35, 30)
)

# Round the body edges
body = body.edges("|Z").fillet(8)
body = body.edges("#Z").fillet(5)

# Top cylinder (nozzle/port going up)
top_cyl = (
    cq.Workplane("XY")
    .workplane(offset=15)
    .circle(8)
    .extrude(20)
    .translate((0, 0, 0))
)

# Side cylinder (port going to the front-left side)
side_cyl = (
    cq.Workplane("YZ")
    .workplane(offset=-20)
    .circle(8)
    .extrude(20)
    .translate((0, -5, -5))
)

# U-channel cutout at the bottom front
u_channel = (
    cq.Workplane("XY")
    .workplane(offset=-15)
    .rect(18, 20)
    .extrude(20)
    .translate((0, 10, 0))
)

# Combine main body with cylinders
result = (
    body
    .union(top_cyl)
    .union(side_cyl)
    .cut(u_channel)
)

# Add rounded edges to the U-channel area
try:
    result = result.edges(cq.selectors.NearestToPointSelector((0, 18, -5))).fillet(4)
except:
    pass

# Actually let's rebuild more carefully
# Main rounded body
body2 = (
    cq.Workplane("XY")
    .box(42, 38, 32)
    .edges("|Z").fillet(9)
    .edges("#Z").fillet(4)
)

# Top port
top_port = (
    cq.Workplane("XY")
    .workplane(offset=16)
    .circle(9)
    .extrude(22)
)

# Side port (pointing in X direction, offset in Y and Z)
side_port = (
    cq.Workplane("YZ")
    .workplane(offset=-21)
    .circle(9)
    .extrude(22)
    .translate((0, -6, -6))
)

# U-shaped slot cut from bottom-front
u_cut = (
    cq.Workplane("XZ")
    .workplane(offset=19)
    .rect(20, 22)
    .extrude(25)
    .translate((0, 0, -5))
)

u_cut2 = (
    cq.Workplane("XZ")
    .workplane(offset=19)
    .circle(10)
    .extrude(20)
    .translate((0, 0, -16))
)

result = (
    body2
    .union(top_port)
    .union(side_port)
    .cut(u_cut)
)

try:
    result = result.edges(
        cq.selectors.BoxSelector((-15, 10, -20), (15, 25, 5))
    ).fillet(3)
except:
    pass