import cadquery as cq
from cadquery import Vector, Edge

# Base block
block = cq.Workplane("XY").box(40, 20, 10)

# Central rod hanging down from bottom face
rod = block.faces("<Z").workplane().center(0, 0).cylinder(60, 1)

result = block.union(rod)

# Parameters for tubes
tube_radius = 0.8
z_top = 10   # top of block
y_front = -8 # front side of block
z_down = -20 # end depth for down tubes

# Straight down tubes
for x in (-12, -4):
    path = Edge.makeSpline([
        Vector(x, y_front, z_top),
        Vector(x, y_front, z_down)
    ])
    tube = cq.Workplane("XY").circle(tube_radius).sweep(path)
    result = result.union(tube)

# Curved tubes looping over block
for x in (4, 12):
    pts = [
        Vector(x,       y_front,     z_top),
        Vector(x,       y_front,     z_top + 8),
        Vector(x + 12,  y_front,     z_top + 8),
        Vector(x + 12,  8,           z_top + 4),
        Vector(x + 12,  8,           -5)
    ]
    path = Edge.makeSpline(pts)
    tube = cq.Workplane("XY").circle(tube_radius).sweep(path)
    result = result.union(tube)

# Final result
result