import cadquery as cq

# Dimensions
wheel_radius = 10
ring_thickness = 3
wheel_thickness = 4
hub_radius = 4
hub_thickness = 2

bar_thickness = 2
bar_width = 4
bar_length = 30
bar_offset_x = 5

handlebar_radius = 1
handlebar_overhang = 6
handlebar_length = bar_offset_x * 2 + handlebar_overhang
handlebar_z = wheel_thickness + bar_length + 2
grip_radius = 1.3
grip_length = 5

pivot_radius = 1.5
pivot_length = bar_offset_x * 2 + 6
pivot_z = wheel_thickness + bar_length / 2

arm_length = 40
arm_width = 4
arm_thickness = 3

# Wheel: rim and hub
rim = (
    cq.Workplane("XY")
    .circle(wheel_radius)
    .extrude(wheel_thickness)
    .cut(
        cq.Workplane("XY")
        .circle(wheel_radius - ring_thickness)
        .extrude(wheel_thickness + 1)
    )
)
hub = (
    cq.Workplane("XY")
    .circle(hub_radius)
    .extrude(hub_thickness)
    .translate((0, 0, (wheel_thickness - hub_thickness) / 2))
)
wheel = rim.union(hub)

# Front wheel
fw = wheel

# Fork bars
bar1 = (
    cq.Workplane("XY")
    .transformed(offset=(bar_offset_x, 0, wheel_thickness))
    .box(bar_thickness, bar_width, bar_length, centered=(True, True, False))
)
bar2 = (
    cq.Workplane("XY")
    .transformed(offset=(-bar_offset_x, 0, wheel_thickness))
    .box(bar_thickness, bar_width, bar_length, centered=(True, True, False))
)
bars = bar1.union(bar2)

# Handlebar
handlebar = (
    cq.Workplane("ZX")
    .circle(handlebar_radius)
    .extrude(handlebar_length, both=True)
    .translate((0, 0, handlebar_z))
)

# Grips
grip1 = (
    cq.Workplane("ZX")
    .transformed(offset=(0, handlebar_length / 2, handlebar_z))
    .circle(grip_radius)
    .extrude(grip_length)
)
grip2 = (
    cq.Workplane("ZX")
    .transformed(offset=(0, -handlebar_length / 2 - grip_length, handlebar_z))
    .circle(grip_radius)
    .extrude(grip_length)
)

# Pivot between fork and arm
pivot = (
    cq.Workplane("YZ")
    .circle(pivot_radius)
    .extrude(pivot_length, both=True)
    .translate((0, 0, pivot_z))
)

# Connecting arm
arm = (
    cq.Workplane("XY")
    .box(arm_width, arm_length, arm_thickness, centered=(True, True, True))
    .translate((0, -arm_length / 2, pivot_z))
)

# Rear wheel
rw = wheel.translate((0, -arm_length, 0))

# Combine all parts
result = fw.union(bars).union(handlebar).union(grip1).union(grip2).union(pivot).union(arm).union(rw)