import cadquery as cq

thickness = 5
small_hole = 5
medium_hole = 8

# 2D outline of the bracket in the XY plane
profile_pts = [
    (0, 0),
    (50, 0),
    (60, 20),
    (60, 80),
    (30, 140),
    (30, 160),
]

# Build the bracket by extruding the profile
result = (
    cq.Workplane("XY")
    .polyline(profile_pts)
    .close()
    .extrude(thickness)
)

# Add small holes at four locations
small_hole_positions = [
    (10, 0),
    (55, 10),
    (45, 110),
    (30, 150),
]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(small_hole_positions)
    .hole(small_hole)
)

# Add the medium hole at the center segment
medium_hole_position = [(60, 50)]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(medium_hole_position)
    .hole(medium_hole)
)