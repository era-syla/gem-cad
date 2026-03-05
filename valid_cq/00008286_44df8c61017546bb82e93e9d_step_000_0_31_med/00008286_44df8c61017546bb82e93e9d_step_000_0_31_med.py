import cadquery as cq

# Wheel Parameters
R_out = 100.0
R_in = 98.0
Rim_width = 5.0

Hub_out = 10.0
Hub_in = 4.0
Hub_width = 8.0

Num_spokes = 24
Spoke_radius = 0.3

# Create the outer rim
rim = (
    cq.Workplane("XY")
    .circle(R_out)
    .circle(R_in)
    .extrude(Rim_width / 2.0, both=True)
)

# Create the central hub
hub = (
    cq.Workplane("XY")
    .circle(Hub_out)
    .circle(Hub_in)
    .extrude(Hub_width / 2.0, both=True)
)

# Combine rim and hub
result = rim.union(hub)

# Create a single reference spoke
# Offset from the inside of the hub and extrude just past the inner rim for a clean boolean union
spoke = (
    cq.Workplane("YZ")
    .workplane(offset=Hub_in)
    .circle(Spoke_radius)
    .extrude(R_in + 1.0 - Hub_in)
)

# Generate the radial spokes and merge them into the final body
for i in range(Num_spokes):
    angle = i * (360.0 / Num_spokes)
    rotated_spoke = spoke.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rotated_spoke)
