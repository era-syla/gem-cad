import cadquery as cq

# Parameters
hex_dia = 10
hex_height = 60
disc_dia = 30
disc_thickness = 4
disc_spacing = 6
num_discs = 4
bottom_cap_thickness = 2
top_cap_thickness = 2

# Central hexagonal shaft
result = cq.Workplane("XY").polygon(6, hex_dia).extrude(hex_height)

# Flanges/discs around the shaft
for i in range(num_discs):
    z = bottom_cap_thickness + disc_spacing + i * (disc_thickness + disc_spacing)
    disc = (
        cq.Workplane("XY")
        .workplane(offset=z)
        .circle(disc_dia / 2)
        .extrude(disc_thickness)
    )
    result = result.union(disc)

# Bottom small cap
bottom_cap = cq.Workplane("XY").circle(hex_dia / 2).extrude(bottom_cap_thickness)
result = result.union(bottom_cap)

# Top small cap
top_cap = (
    cq.Workplane("XY")
    .workplane(offset=hex_height)
    .circle(hex_dia / 2)
    .extrude(top_cap_thickness)
)
result = result.union(top_cap)