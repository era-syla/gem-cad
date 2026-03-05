import cadquery as cq

# Base plate
base = (
    cq.Workplane("XY")
    .rect(100, 30)
    .extrude(5)
    .faces(">Z")
    .workplane()
    .pushPoints([(-35, 15), (-35, -15), (35, 15), (35, -15)])
    .hole(6)
)

# Lower bracket plates
lb1 = (
    cq.Workplane("XY")
    .transformed(offset=(-20, 10, 5))
    .rect(10, 4)
    .extrude(30)
)
lb2 = (
    cq.Workplane("XY")
    .transformed(offset=(-20, -10, 5))
    .rect(10, 4)
    .extrude(30)
)

# Pivot pin between lower plates
pin = (
    cq.Workplane("YZ")
    .transformed(offset=(-20, 0, 20))
    .circle(4)
    .extrude(20)
)

# Link block connecting pivot to handle
link_block = (
    cq.Workplane("XY")
    .transformed(offset=(-5, 0, 25))
    .rect(30, 4)
    .extrude(8)
    .faces(">Z")
    .workplane()
    .pushPoints([(-15, 0), (15, 0)])
    .hole(6)
)

# Handle: cylindrical grip + spherical end
handle_cyl = (
    cq.Workplane("YZ")
    .transformed(offset=(10, 0, 29))
    .circle(6)
    .extrude(80)
)
handle_sphere = (
    cq.Workplane("XY")
    .transformed(offset=(90, 0, 29))
    .sphere(6)
)
handle = handle_cyl.union(handle_sphere)

# Clamp foot on the other side of pivot
foot_cyl = (
    cq.Workplane("YZ")
    .transformed(offset=(-20, 0, 20))
    .circle(5)
    .extrude(-40)
)
foot_sphere = (
    cq.Workplane("XY")
    .transformed(offset=(-60, 0, 20))
    .sphere(5)
)
foot = foot_cyl.union(foot_sphere)

# Combine all parts
result = base.union(lb1).union(lb2).union(pin).union(link_block).union(handle).union(foot)