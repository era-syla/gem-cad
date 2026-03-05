import cadquery as cq

n = 6
radius = 10
cyl_height = 40
cone_height = 10
base_thickness = 5
base_width = 20
spacing = 2 * radius + 5
margin = 5
base_length = (n - 1) * spacing + 2 * radius + 2 * margin

positions = [
    (-base_length / 2 + margin + radius + i * spacing, 0, 0)
    for i in range(n)
]

base = cq.Workplane("XY").box(base_length, base_width, base_thickness)

rod = (
    cq.Workplane("XZ")
    .moveTo(radius, base_thickness)
    .lineTo(radius, base_thickness + cyl_height)
    .lineTo(0, base_thickness + cyl_height + cone_height)
    .lineTo(0, base_thickness)
    .close()
    .revolve(360, (0, 0, 0), (0, 0, 1))
)

result = base
for pos in positions:
    result = result.union(rod.translate(pos))