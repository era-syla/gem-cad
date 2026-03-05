import cadquery as cq

# Parameters
thickness = 5    # plate thickness
height = 50      # vertical plate height
depth = 30       # horizontal flange depth
fillet_r = 2     # edge fillet radius
hole_d = 6       # hole diameter
y_mid = thickness/2
hole_z1 = height * 0.3
hole_z2 = height * 0.7

# Create L‐bracket cross section in YZ and extrude in X
bracket = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),
        (depth, 0),
        (depth, thickness),
        (thickness, thickness),
        (thickness, height),
        (0, height),
    ])
    .close()
    .extrude(thickness)
)

# Create hole cutters and subtract
cutter1 = (
    cq.Workplane("YZ")
    .center(y_mid, hole_z1)
    .circle(hole_d/2)
    .extrude(thickness)
)
cutter2 = (
    cq.Workplane("YZ")
    .center(y_mid, hole_z2)
    .circle(hole_d/2)
    .extrude(thickness)
)

result = (
    bracket
    .cut(cutter1)
    .cut(cutter2)
    .edges()
    .fillet(fillet_r)
)