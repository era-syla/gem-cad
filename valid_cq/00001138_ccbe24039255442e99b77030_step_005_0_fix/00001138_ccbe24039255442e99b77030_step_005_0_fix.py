import cadquery as cq

def make_pipe(path_pts, r):
    edges = []
    for a, b in zip(path_pts, path_pts[1:]):
        edges.append(cq.Edge.makeLine(cq.Vector(*a), cq.Vector(*b)))
    path_wire = cq.Wire.combine(edges)[0]
    start = path_pts[0]
    return cq.Workplane('XY').transformed(offset=cq.Vector(*start)).circle(r).sweep(path_wire)

tube_radius = 1.5

segments = []

# Main left rail
left2d = [(0, 0), (100, 0), (130, 20), (160, 40)]
segments.append([(x, 0, z) for x, z in left2d])

# Main right rail
segments.append([(x, 30, z) for x, z in left2d])

# Front bumper
segments.append([
    (160, 0, 40),
    (165, 0, 45),
    (165, 30, 45),
    (160, 30, 40)
])

# Rear loop
segments.append([
    (10, 0, 0),
    (10, 0, 40),
    (30, 0, 40),
    (30, 30, 40),
    (10, 30, 40),
    (10, 30, 0)
])

# Cross braces
segments.append([(50, 0, 0), (50, 30, 0)])
segments.append([(80, 0, 0), (80, 30, 0)])

# Diagonal braces
segments.append([(50, 0, 0), (110, 30, 20)])
segments.append([(80, 0, 0), (130, 30, 20)])

pipes = [make_pipe(path, tube_radius) for path in segments]

result = pipes[0]
for p in pipes[1:]:
    result = result.union(p)