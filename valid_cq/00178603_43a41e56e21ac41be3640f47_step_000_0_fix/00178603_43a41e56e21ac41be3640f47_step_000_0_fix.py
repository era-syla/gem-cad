import cadquery as cq
from cadquery import Vector

# Handle (hollow tube)
handle_outer = cq.Workplane("XY").circle(3).extrude(20)
handle_inner = cq.Workplane("XY").circle(2.5).extrude(20)
handle = handle_outer.cut(handle_inner)

# Define arm path points (one side)
pts1 = [
    Vector(0, 0, 20),
    Vector(5, 2, 35),
    Vector(10, 5, 50),
    Vector(18, 8, 60),
    Vector(20, 10, 62),
    Vector(17, 8, 64),
]
# Mirrored path for the other arm
pts2 = [Vector(-p.x, p.y, p.z) for p in pts1]

path1 = cq.Edge.makeSpline(pts1)
path2 = cq.Edge.makeSpline(pts2)

# Sweep solid arms
arm1 = cq.Workplane("XY").workplane(offset=20).circle(1.5).sweep(path1)
arm2 = cq.Workplane("XY").workplane(offset=20).circle(1.5).sweep(path2)

# Combine everything
result = handle.union(arm1).union(arm2)