import cadquery as cq

# Parameters
chain_length = 120.0
seat_length = 120.0
chain_offset = -20.0
seat_offset = 20.0
tube_radius = 5.0
dropout_plate_width = 20.0
dropout_plate_thickness = 8.0
boss_radius = 8.0
boss_height = 12.0

# Chainstay path
chain_path = (
    cq.Workplane("XY")
    .polyline([(0, 0), (chain_length, chain_offset)])
    .wire()
)

# Seatstay path
seat_path = (
    cq.Workplane("XY")
    .polyline([(0, 0), (seat_length, seat_offset)])
    .wire()
)

# Create chainstay tube
chainstay = (
    cq.Workplane("XY")
    .circle(tube_radius)
    .sweep(chain_path, multisection=False)
)

# Create seatstay tube
seatstay = (
    cq.Workplane("XY")
    .circle(tube_radius)
    .sweep(seat_path, multisection=False)
)

# Dropout plate at chainstay end
dropout = (
    cq.Workplane("XY")
    .transformed(offset=(chain_length, chain_offset, 0))
    .rect(dropout_plate_width, dropout_plate_width / 2)
    .extrude(dropout_plate_thickness)
)

# Pivot boss at seatstay end
boss = (
    cq.Workplane("XY")
    .transformed(offset=(seat_length, seat_offset, 0))
    .circle(boss_radius)
    .extrude(boss_height)
)

# Combine all parts
result = chainstay.union(seatstay).union(dropout).union(boss)