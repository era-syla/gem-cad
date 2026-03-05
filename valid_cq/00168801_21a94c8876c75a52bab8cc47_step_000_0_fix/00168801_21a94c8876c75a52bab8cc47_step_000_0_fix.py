import cadquery as cq

plate_thickness = 5.0

points = [
    (-100, -100),
    (-20, -100),
    (-20, -120),
    (20, -120),
    (20, -100),
    (100, -100),
    (100, -20),
    (120, -20),
    (120, 20),
    (100, 20),
    (100, 100),
    (20, 100),
    (20, 120),
    (-20, 120),
    (-20, 100),
    (-100, 100),
    (-100, 20),
    (-120, 20),
    (-120, -20),
    (-100, -20),
]

result = cq.Workplane("XY").polyline(points).close().extrude(plate_thickness)

# Central hole
result = result.faces(">Z").workplane().hole(20)

# Grid of small holes
grid_pts = [(x, y) for x in (-40, 0, 40) for y in (-40, 0, 40)]
result = result.faces(">Z").workplane().pushPoints(grid_pts).hole(5)

# Tab holes
tab_pts = [(0, -120), (120, 0), (0, 120), (-120, 0)]
result = result.faces(">Z").workplane().pushPoints(tab_pts).hole(5)

# Corner holes
corner_pts = [(-80, -80), (80, -80), (80, 80), (-80, 80)]
result = result.faces(">Z").workplane().pushPoints(corner_pts).hole(5)