import cadquery as cq

# Parameters
plate_x = 100
plate_y = 80
plate_thickness = 3
hex_r = 4
hex_margin = 10
nx = 5
ny = 7

x_spacing = plate_x - 2 * hex_margin
y_spacing = plate_y - 2 * hex_margin

motor_positions = [
    (-x_spacing/2, -y_spacing/2),
    ( x_spacing/2, -y_spacing/2),
    ( x_spacing/2,  y_spacing/2),
    (-x_spacing/2,  y_spacing/2),
]

duct_outer_d = 30
wall_thickness = 2
inner_d = duct_outer_d - 2 * wall_thickness
duct_height = 8

hub_od = 12
hub_id = 6
spoke_width = 3

r_inner = inner_d / 2
r_hub = hub_od / 2
spoke_length = r_inner - r_hub

# Start with the central plate
plate = cq.Workplane("XY").box(plate_x, plate_y, plate_thickness)

# Honeycomb pattern cutouts
hx_spacing = (plate_x - 2 * hex_margin) / (nx - 1)
hy_spacing = (plate_y - 2 * hex_margin) / (ny - 1)
points = []
for i in range(nx):
    for j in range(ny):
        x_hex = -plate_x/2 + hex_margin + i * hx_spacing
        y_hex = -plate_y/2 + hex_margin + j * hy_spacing
        points.append((x_hex, y_hex))

plate = plate.faces(">Z") \
    .workplane() \
    .pushPoints(points) \
    .polygon(6, hex_r) \
    .cutThruAll()

# Add ducts, hubs, and spokes at motor positions
result = plate
for px, py in motor_positions:
    # Outer duct wall
    result = result.union(
        cq.Workplane("XY")
        .transformed(offset=(px, py, plate_thickness/2))
        .circle(duct_outer_d/2)
        .extrude(duct_height)
    )
    # Inner duct cutout
    result = result.cut(
        cq.Workplane("XY")
        .transformed(offset=(px, py, plate_thickness/2))
        .circle(inner_d/2)
        .extrude(duct_height)
    )
    # Motor hub
    result = result.union(
        cq.Workplane("XY")
        .transformed(offset=(px, py, plate_thickness/2))
        .circle(hub_od/2)
        .extrude(duct_height)
    )
    # Hub bore
    result = result.cut(
        cq.Workplane("XY")
        .transformed(offset=(px, py, plate_thickness/2))
        .circle(hub_id/2)
        .extrude(duct_height)
    )
    # Spokes
    for angle in (0, 120, 240):
        result = result.union(
            cq.Workplane("XY")
            .transformed(offset=(px, py, plate_thickness/2), rotate=(0, 0, angle))
            .center(r_hub + spoke_length/2, 0)
            .rect(spoke_length, spoke_width)
            .extrude(duct_height)
        )

result