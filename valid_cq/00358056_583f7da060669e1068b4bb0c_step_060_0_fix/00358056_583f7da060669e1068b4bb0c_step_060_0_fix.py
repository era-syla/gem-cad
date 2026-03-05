import cadquery as cq

# Parameters
plate_thickness = 3
h_length = 200
h_width = 20
v_width = 20
v_height = 150
hole_dia = 4
hole_margin_x = 5
hole_margin_z = 10
hole_count = 8

# Create horizontal base plate
base = cq.Workplane("XY").rect(h_length, h_width).extrude(plate_thickness)

# Create vertical plate
vertical = (
    cq.Workplane("XZ", origin=(0, -h_width / 2, plate_thickness))
    .rect(v_width, v_height)
    .extrude(h_width)
)

# Drill holes in vertical plate
spacing_z = (v_height - 2 * hole_margin_z) / (hole_count - 1)
x_offsets = [
    -v_width / 2 + hole_margin_x,
    v_width / 2 - hole_margin_x
]
points = []
for i in range(hole_count):
    z_rel = -v_height / 2 + hole_margin_z + i * spacing_z
    for x in x_offsets:
        points.append((x, z_rel))

vertical = (
    vertical.faces(">Y")
    .workplane()
    .pushPoints(points)
    .hole(hole_dia, plate_thickness + 1)
)

# Combine parts
result = base.union(vertical)