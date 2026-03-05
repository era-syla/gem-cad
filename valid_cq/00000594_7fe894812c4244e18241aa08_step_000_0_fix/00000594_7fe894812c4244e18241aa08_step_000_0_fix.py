import cadquery as cq

# Main body - rectangular block
body = (
    cq.Workplane("XY")
    .box(25, 20, 18)
)

# Add the cylindrical inlet tube on the front/left side
inlet_tube = (
    cq.Workplane("YZ")
    .workplane(offset=-12.5)
    .circle(7)
    .extrude(12)
)

# Add the outlet tube going down
outlet_tube = (
    cq.Workplane("XY")
    .workplane(offset=-9)
    .circle(5.5)
    .extrude(10)
)

# Combine body with tubes
result = body.union(inlet_tube).union(outlet_tube)

# Hollow out the inlet tube
result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=-12.5)
    .circle(5)
    .extrude(30)
)

# Hollow out the outlet tube
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=-9)
    .circle(4)
    .extrude(20)
)

# Add collar/flange ring around inlet
collar = (
    cq.Workplane("YZ")
    .workplane(offset=2)
    .circle(9)
    .circle(7)
    .extrude(3)
)
result = result.union(collar)

# Add adjustment screw housing on top right
screw_housing = (
    cq.Workplane("XY")
    .workplane(offset=9)
    .center(8, 0)
    .circle(3)
    .extrude(15)
)
result = result.union(screw_housing)

# Add knurled knob on top of screw
knob = (
    cq.Workplane("XY")
    .workplane(offset=24)
    .center(8, 0)
    .circle(5)
    .extrude(8)
)
result = result.union(knob)

# Add side valve/fitting on the left side of body
side_fitting = (
    cq.Workplane("XZ")
    .workplane(offset=-10)
    .center(0, 0)
    .circle(5)
    .extrude(8)
)
result = result.union(side_fitting)

# Add nut hex around side fitting
hex_nut = (
    cq.Workplane("XZ")
    .workplane(offset=-12)
    .center(0, 0)
    .polygon(6, 14)
    .extrude(4)
)
result = result.union(hex_nut)

# Cut hole through side fitting
result = result.cut(
    cq.Workplane("XZ")
    .workplane(offset=-14)
    .center(0, 0)
    .circle(2.5)
    .extrude(20)
)

# Add lever arm on the side
lever_base = (
    cq.Workplane("XZ")
    .workplane(offset=-8)
    .center(0, -6)
    .circle(4)
    .extrude(4)
)
result = result.union(lever_base)

# Lever arm extending down
lever_arm = (
    cq.Workplane("XZ")
    .workplane(offset=-8)
    .center(0, -6)
    .rect(3, 18)
    .extrude(3)
)
result = result.union(lever_arm)

# Mounting tab at end of lever
mount_tab = (
    cq.Workplane("XZ")
    .workplane(offset=-8)
    .center(5, -17)
    .circle(5)
    .extrude(3)
)
result = result.union(mount_tab)

# Hole in mounting tab
result = result.cut(
    cq.Workplane("XZ")
    .workplane(offset=-8)
    .center(5, -17)
    .circle(2)
    .extrude(5)
)

# Add second mounting tab
mount_tab2 = (
    cq.Workplane("XZ")
    .workplane(offset=-8)
    .center(-5, -17)
    .circle(5)
    .extrude(3)
)
result = result.union(mount_tab2)

result = result.cut(
    cq.Workplane("XZ")
    .workplane(offset=-8)
    .center(-5, -17)
    .circle(2)
    .extrude(5)
)

# Add screws on top of body
for x_off in [-6, 6]:
    screw = (
        cq.Workplane("XY")
        .workplane(offset=9)
        .center(x_off, 7)
        .circle(2)
        .extrude(4)
    )
    result = result.union(screw)