import cadquery as cq

# Parameters
num_rods = 5
rod_radius = 2.5
rod_length = 150
spacing = 6.0  # center-to-center spacing

# Build a bundle of parallel cylindrical rods
result = cq.Workplane("XY")

rods = None

for i in range(num_rods):
    x_offset = (i - (num_rods - 1) / 2.0) * spacing
    rod = (
        cq.Workplane("XY")
        .center(x_offset, 0)
        .circle(rod_radius)
        .extrude(rod_length)
    )
    if rods is None:
        rods = rod
    else:
        rods = rods.union(rod)

result = rods