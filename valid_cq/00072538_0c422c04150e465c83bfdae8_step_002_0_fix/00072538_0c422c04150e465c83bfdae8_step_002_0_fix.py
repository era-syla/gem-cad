import cadquery as cq

# Parameters
radius_main = 15
head_radius = 22
head_bottom_z = 0
head_top_z = 100
seat_top_z = 280
seat_x = 200

# Head tube
head = cq.Workplane("XY") \
    .center(0, 0) \
    .circle(head_radius) \
    .extrude(head_top_z)

# Top tube
top = (
    cq.Workplane("XY")
    .workplane(offset=head_top_z)
    .center(0, 0)
    .circle(radius_main)
    .workplane(offset=seat_top_z)
    .center(seat_x, 0)
    .circle(radius_main)
    .loft()
)

# Down tube
down = (
    cq.Workplane("XY")
    .workplane(offset=head_bottom_z)
    .center(0, 0)
    .circle(radius_main)
    .workplane(offset=seat_top_z)
    .center(seat_x, 0)
    .circle(radius_main)
    .loft()
)

# Seat tube
seat = (
    cq.Workplane("XY")
    .workplane(offset=head_bottom_z)
    .center(seat_x, 0)
    .circle(radius_main)
    .workplane(offset=seat_top_z)
    .center(seat_x, 0)
    .circle(radius_main)
    .loft()
)

# Cable stop / mount cylinders on seat tube
mounts = None
for z in (100, 180):
    m = (
        cq.Workplane("XY")
        .transformed(offset=(seat_x + radius_main, 0, z), rotate=(0, 90, 0))
        .circle(4)
        .extrude(8)
    )
    mounts = m if mounts is None else mounts.union(m)

# Combine all parts
result = head.union(top).union(down).union(seat).union(mounts)