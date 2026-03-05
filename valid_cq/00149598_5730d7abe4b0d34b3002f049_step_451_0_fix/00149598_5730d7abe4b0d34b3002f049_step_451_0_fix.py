import cadquery as cq

# Parameters
thickness = 5.0
large_hole_dia = 20.0
mid_hole_dia = 5.0
corner_hole_dia = 3.0

# Base plate profile in the XY plane
result = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (120, 0),
        (120, 80),
        (20, 80),
        (0, 60),
    ])
    .close()
    .extrude(thickness)
    # Top face operations
    .faces(">Z")
    .workplane()
    # Large central hole
    .pushPoints([(30, 20)])
    .hole(large_hole_dia)
    # Two mid-size holes around the large hole
    .pushPoints([(50, 40), (40, 20)])
    .hole(mid_hole_dia)
    # Small corner holes at each vertex
    .pushPoints([
        (5, 5),
        (115, 5),
        (115, 75),
        (25, 75),
        (5, 55),
    ])
    .hole(corner_hole_dia)
)

# `result` now holds the final solid
