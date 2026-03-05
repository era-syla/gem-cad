import cadquery as cq

thickness = 6
small_hole = 5
center_hole = 12
plate_w = 40
plate_h = 40

# L-shaped bracket
l_points = [(0, 0), (30, 0), (30, 10), (10, 10), (10, 40), (0, 40)]
l_bracket = cq.Workplane("XY").polyline(l_points).close().extrude(thickness)
l_bracket = (
    l_bracket
    .faces(">Z")
    .workplane()
    .pushPoints([(5, 35), (25, 5)])
    .hole(small_hole)
)

# Rectangular plate with two holes at top
plate2 = cq.Workplane("XY").rect(plate_w, plate_h).extrude(thickness)
plate2 = (
    plate2
    .faces(">Z")
    .workplane()
    .pushPoints([(-10, 15), (10, 15)])
    .hole(small_hole)
)

# Rectangular plate with a single center hole
plate3 = cq.Workplane("XY").rect(plate_w, plate_h).extrude(thickness)
plate3 = (
    plate3
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 0)])
    .hole(center_hole)
)

# Rectangular plate with four corner holes and a center hole
plate4 = cq.Workplane("XY").rect(plate_w, plate_h).extrude(thickness)
plate4 = plate4.faces(">Z").workplane()
corner_pts = [(-10, 15), (10, 15), (-10, -15), (10, -15)]
plate4 = plate4.pushPoints(corner_pts).hole(small_hole)
plate4 = plate4.pushPoints([(0, 0)]).hole(center_hole)

# Assemble all parts side by side
result = (
    l_bracket.translate((-60, 0, 0))
    .union(plate2.translate((-20, 0, 0)))
    .union(plate3.translate((20, 0, 0)))
    .union(plate4.translate((60, 0, 0)))
)