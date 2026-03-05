import cadquery as cq

flange_outer_radius = 15
tube_outer_radius = 10
tube_inner_radius = 5
tube_length = 50
flange_thickness = 3

profile = [
    (0, 0),
    (flange_thickness, 0),
    (flange_thickness, tube_inner_radius),
    (flange_thickness + tube_length, tube_inner_radius),
    (flange_thickness + tube_length, tube_outer_radius),
    (flange_thickness, tube_outer_radius),
    (flange_thickness, flange_outer_radius),
    (0, flange_outer_radius),
]

result = (
    cq.Workplane("XZ")
    .polyline(profile)
    .close()
    .revolve(360, axisStart=(0, 0, 0), axisEnd=(1, 0, 0))
)