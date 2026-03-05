import cadquery as cq

# Base plate
back = cq.Workplane("YZ").rect(60, 10).extrude(5)

# Wavy shelf/profile
wave = back.faces(">X").workplane().polyline([
    (0, 0),
    (20, 10),
    (40, 5),
    (60, 15),
    (80, 0),
    (100, 5),
    (100, -5),
    (60, -15),
    (40, -5),
    (20, -10),
    (0, 0)
]).close().extrude(3)

# Thin rod, extruded then rotated
rod = cq.Workplane("YZ").center(20, 0).circle(0.5).extrude(100).rotate((0, 0, 0), (0, 1, 0), 20)

# Combine everything
result = back.union(wave).union(rod)