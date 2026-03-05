import cadquery as cq

# Stepper motor model
# Main body dimensions
body_size = 42  # mm (NEMA 17 style)
body_height = 48
flange_thickness = 3
flange_overhang = 4
shaft_diameter = 5
shaft_height = 24
boss_diameter = 22
boss_height = 2
corner_radius = 3
mount_hole_diameter = 3
mount_hole_offset = 31 / 2  # from center

# Main body - slightly rounded square cross section
body = (
    cq.Workplane("XY")
    .box(body_size, body_size, body_height)
)

# Add corner fillets to the body
body = body.edges("|Z").fillet(corner_radius)

# Top flange plate
flange_size = body_size + flange_overhang * 2
flange = (
    cq.Workplane("XY")
    .workplane(offset=body_height / 2)
    .box(flange_size, flange_size, flange_thickness)
    .translate((0, 0, flange_thickness / 2))
)

# Translate flange to sit on top of body
flange_z = body_height / 2 + flange_thickness / 2
flange = (
    cq.Workplane("XY")
    .workplane(offset=flange_z)
    .rect(flange_size, flange_size)
    .extrude(flange_thickness)
    .translate((0, 0, 0))
)

# Build flange as a box at correct Z
flange_solid = (
    cq.Workplane("XY")
    .box(flange_size, flange_size, flange_thickness)
    .translate((0, 0, body_height / 2 + flange_thickness / 2))
)

# Add corner fillets to flange
flange_solid = flange_solid.edges("|Z").fillet(corner_radius)

# Combine body and flange
result = body.union(flange_solid)

# Boss (circular hub on top of flange)
boss_z = body_height / 2 + flange_thickness
boss = (
    cq.Workplane("XY")
    .workplane(offset=boss_z)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

result = result.union(boss)

# Shaft on top of boss
shaft_z = boss_z + boss_height
shaft = (
    cq.Workplane("XY")
    .workplane(offset=shaft_z)
    .circle(shaft_diameter / 2)
    .extrude(shaft_height)
)

result = result.union(shaft)

# Mounting holes in the flange (4 corners)
hole_z = body_height / 2 + flange_thickness
hole_positions = [
    (mount_hole_offset, mount_hole_offset),
    (-mount_hole_offset, mount_hole_offset),
    (mount_hole_offset, -mount_hole_offset),
    (-mount_hole_offset, -mount_hole_offset),
]

for hx, hy in hole_positions:
    hole = (
        cq.Workplane("XY")
        .workplane(offset=hole_z - flange_thickness)
        .center(hx, hy)
        .circle(mount_hole_diameter / 2)
        .extrude(flange_thickness + 0.1)
    )
    result = result.cut(hole)

# Small connector/cable hole indicator on front face (small rectangular protrusion)
# Connector box on one side (small rectangular bump on lower portion)
connector_w = 14
connector_h = 8
connector_d = 2
connector_z = -body_height / 2 + connector_h / 2 + 4

connector = (
    cq.Workplane("XY")
    .workplane(offset=connector_z)
    .transformed(offset=cq.Vector(0, body_size / 2 + connector_d / 2, 0))
    .rect(connector_w, connector_d)
    .extrude(connector_h)
    .translate((0, 0, 0))
)

# Build connector properly
connector = (
    cq.Workplane("YZ")
    .workplane(offset=body_size / 2)
    .center(0, connector_z)
    .rect(connector_w, connector_h)
    .extrude(connector_d)
)

result = result.union(connector)

# Corner bracket details - small rectangular tabs at base corners
tab_size = 6
tab_height = 8
tab_thickness = 3

for sx, sy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
    tab = (
        cq.Workplane("XY")
        .box(tab_size, tab_thickness, tab_height)
        .translate((
            sx * (body_size / 2 + tab_size / 2 - tab_size / 2),
            sy * (body_size / 2 + tab_thickness / 2 - tab_thickness / 2),
            -body_height / 2 + tab_height / 2
        ))
    )