import cadquery as cq

# Main box body
box_l = 60
box_w = 40
box_h = 25

# Create the main body with fillets
body = (
    cq.Workplane("XY")
    .box(box_l, box_w, box_h)
    .edges("|Z")
    .fillet(5)
    .edges(">Z or <Z")
    .fillet(2)
)

# Add corner screws/bolts on top (4 corners)
screw_offset_x = 22
screw_offset_y = 14
screw_r = 4
screw_h = 4

corner_positions = [
    (screw_offset_x, screw_offset_y),
    (-screw_offset_x, screw_offset_y),
    (screw_offset_x, -screw_offset_y),
    (-screw_offset_x, -screw_offset_y),
]

for (cx, cy) in corner_positions:
    cap = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(cx, cy, box_h / 2))
        .cylinder(screw_h, screw_r)
    )
    body = body.union(cap)

# Add connectors on the sides (left and right, 2 on each side)
connector_r = 5
connector_h = 10
connector_offset_y = 10

# Left side connectors (negative X direction)
for cy in [connector_offset_y, -connector_offset_y]:
    conn = (
        cq.Workplane("YZ")
        .transformed(offset=cq.Vector(cy, 0, 0))
        .workplane()
        .transformed(offset=cq.Vector(0, 0, -box_l / 2 - connector_h / 2))
        .cylinder(connector_h, connector_r)
    )
    body = body.union(conn)

# Right side connectors (positive X direction)
for cy in [connector_offset_y, -connector_offset_y]:
    conn = (
        cq.Workplane("YZ")
        .transformed(offset=cq.Vector(cy, 0, 0))
        .workplane()
        .transformed(offset=cq.Vector(0, 0, box_l / 2 + connector_h / 2))
        .cylinder(connector_h, connector_r)
    )
    body = body.union(conn)

# Add knurling detail rings on connectors (simplified as slightly larger rings)
ring_r = connector_r + 0.8
ring_h = 2

# Left connectors rings
for cy in [connector_offset_y, -connector_offset_y]:
    for rx in [-box_l / 2 - 2, -box_l / 2 - 6]:
        ring = (
            cq.Workplane("XY")
            .transformed(offset=cq.Vector(rx, cy, 0))
            .cylinder(ring_h, ring_r)
        )
        body = body.union(ring)

# Right connectors rings
for cy in [connector_offset_y, -connector_offset_y]:
    for rx in [box_l / 2 + 2, box_l / 2 + 6]:
        ring = (
            cq.Workplane("XY")
            .transformed(offset=cq.Vector(rx, cy, 0))
            .cylinder(ring_h, ring_r)
        )
        body = body.union(ring)

# Add holes on top surface
top_holes = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, box_h / 2))
    .pushPoints([(-8, 0), (8, 0)])
    .circle(3)
    .extrude(8)
)

body = body.cut(top_holes)

# Add holes through connectors
# Left side
for cy in [connector_offset_y, -connector_offset_y]:
    hole = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(-box_l / 2 - connector_h, cy, 0))
        .cylinder(connector_h + 5, 2.5)
    )
    body = body.cut(hole)

# Right side
for cy in [connector_offset_y, -connector_offset_y]:
    hole = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(box_l / 2 + connector_h, cy, 0))
        .cylinder(connector_h + 5, 2.5)
    )
    body = body.cut(hole)

result = body