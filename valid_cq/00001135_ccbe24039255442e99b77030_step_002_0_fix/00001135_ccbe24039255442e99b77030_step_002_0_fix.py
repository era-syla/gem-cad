import cadquery as cq
from math import acos, degrees

def cylinder_between(a, b, r):
    v = b - a
    h = v.Length
    u = v.normalized()
    cyl = cq.Workplane("XY").circle(r).extrude(h).translate((0, 0, -h/2))
    z = cq.Vector(0, 0, 1)
    dot = z.dot(u)
    if abs(abs(dot) - 1) < 1e-6:
        if dot < 0:
            cyl = cyl.rotate((0, 0, 0), (1, 0, 0), 180)
    else:
        axis = z.cross(u)
        angle = degrees(acos(dot))
        cyl = cyl.rotate((0, 0, 0), axis.toTuple(), angle)
    mid = a + v * 0.5
    cyl = cyl.translate(mid.toTuple())
    return cyl

# Define key points
nodes = {
    'bbl': cq.Vector(-40, -50, 0),
    'bbr': cq.Vector( 40, -50, 0),
    'btl': cq.Vector(-40, -50, 50),
    'btr': cq.Vector( 40, -50, 50),
    'fbl': cq.Vector(-40,  50, 0),
    'fbr': cq.Vector( 40,  50, 0),
    'ftl': cq.Vector(-40,  50, 50),
    'ftr': cq.Vector( 40,  50, 50),
}

# Define tube connections
segments = [
    ('bbl', 'bbr'),
    ('bbl', 'btl'),
    ('bbr', 'btr'),
    ('bbl', 'fbl'),
    ('bbr', 'fbr'),
    ('fbl', 'ftl'),
    ('fbr', 'ftr'),
    ('btl', 'btr'),
    ('ftl', 'ftr'),
    ('btl', 'fbl'),
    ('btr', 'fbr'),
    ('btl', 'ftr'),
    ('btr', 'ftl'),
]

tube_radius = 2.5
result = None
for a_key, b_key in segments:
    a = nodes[a_key]
    b = nodes[b_key]
    cyl = cylinder_between(a, b, tube_radius)
    if result is None:
        result = cyl
    else:
        result = result.union(cyl)