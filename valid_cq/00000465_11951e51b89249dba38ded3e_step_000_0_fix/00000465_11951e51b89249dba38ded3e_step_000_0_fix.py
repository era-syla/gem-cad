import cadquery as cq

# Main cylinder body
main_cylinder = (
    cq.Workplane("XY")
    .cylinder(80, 8)
)

# Inner rod (smaller cylinder extending from one end)
inner_rod = (
    cq.Workplane("XY")
    .workplane(offset=40)
    .circle(4)
    .extrude(50)
)

# Combine main cylinder and rod
body = main_cylinder.union(inner_rod)

# Add a collar/ring near the rod end
collar1 = (
    cq.Workplane("XY")
    .workplane(offset=35)
    .circle(9)
    .extrude(5)
)

body = body.union(collar1)

# Add another collar
collar2 = (
    cq.Workplane("XY")
    .workplane(offset=25)
    .circle(9)
    .extrude(5)
)

body = body.union(collar2)

# End cap / clevis mount at the negative end (fork end)
# Base of clevis
clevis_base = (
    cq.Workplane("XY")
    .workplane(offset=-40)
    .circle(8)
    .extrude(8)
)

body = body.union(clevis_base)

# Clevis fork - two prongs
prong1 = (
    cq.Workplane("XZ")
    .workplane(offset=6)
    .center(0, -44)
    .box(4, 16, 10)
)

prong2 = (
    cq.Workplane("XZ")
    .workplane(offset=-6)
    .center(0, -44)
    .box(4, 16, 10)
)

body = body.union(prong1).union(prong2)

# Pin through clevis
pin = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .center(-44, 0)
    .circle(3)
    .extrude(20)
    .translate((0, 0, 0))
)

# Actually build clevis pin along Y axis
clevis_pin = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .center(0, -44)
    .circle(2.5)
    .extrude(20)
)

body = body.union(clevis_pin)

# Small knob/bolt at bottom of clevis
knob = (
    cq.Workplane("XY")
    .workplane(offset=-56)
    .circle(4)
    .extrude(6)
)

body = body.union(knob)

# Rod end connector (clevis eye) at the rod tip
rod_tip_z = 90
eye_base = (
    cq.Workplane("XY")
    .workplane(offset=rod_tip_z)
    .circle(5)
    .extrude(6)
)

body = body.union(eye_base)

# Eye ring at tip
eye_ring = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .center(rod_tip_z + 6, 0)
    .circle(5)
    .extrude(3)
    .translate((0, 0, 0))
)

# Build eye ring properly
eye_outer = (
    cq.Workplane("XY")
    .workplane(offset=rod_tip_z + 4)
    .circle(6)
    .extrude(8)
)

eye_inner = (
    cq.Workplane("XY")
    .workplane(offset=rod_tip_z + 3)
    .circle(3.5)
    .extrude(10)
)

eye_ring_solid = eye_outer.cut(eye_inner)

body = body.union(eye_ring_solid)

result = body