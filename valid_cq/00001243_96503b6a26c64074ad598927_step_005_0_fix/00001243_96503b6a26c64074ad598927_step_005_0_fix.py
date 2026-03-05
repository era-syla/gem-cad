import cadquery as cq

blade_length = 120.0
thickness = 2.0
half_thick = thickness/2
width = 8.0
tang_length = 30.0
bevel_start = 35.0
bevel_flat_length = 70.0

profile = [
    (0, -half_thick),
    (0, half_thick),
    (tang_length, half_thick),
    (bevel_start, half_thick * 0.8),
    (bevel_start + bevel_flat_length, half_thick * 0.8),
    (blade_length, 0),
    (bevel_start + bevel_flat_length, -half_thick * 0.8),
    (bevel_start, -half_thick * 0.8),
    (tang_length, -half_thick),
    (0, -half_thick),
]

result = (
    cq.Workplane("XZ")
    .polyline(profile)
    .close()
    .extrude(width)
    .translate((0, -width/2, 0))
)