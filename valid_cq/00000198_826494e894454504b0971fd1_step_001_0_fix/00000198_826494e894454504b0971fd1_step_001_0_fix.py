import cadquery as cq
import math

thickness = 6
R = 35
node_r = 8

# Define node centers
angles = [180, 60, -60]
pts = [(R * math.cos(math.radians(a)), R * math.sin(math.radians(a))) for a in angles]

# Create plate outline by offsetting a polyline
plate = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .offset2D(node_r)
    .extrude(thickness)
)

# Add circular holes at each node and center hole
plate = (
    plate
    .faces(">Z")
    .workplane()
    .pushPoints(pts + [(0, 0)])
    .hole(5)
)

# Add triangular cutouts between nodes
for i in range(len(pts)):
    p1 = pts[i]
    p2 = pts[(i + 1) % len(pts)]
    plate = (
        plate
        .faces(">Z")
        .workplane()
        .polyline([p1, p2, (0, 0)])
        .close()
        .cutThruAll()
    )

# Fillet vertical edges
plate = plate.edges("|Z").fillet(2)

# Create tube on the first node (angle 180)
tube_outer = 12
tube_inner = 8
tube_length = 20
tube_center = pts[0]

tube = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(tube_center[0], tube_center[1])
    .circle(tube_outer / 2)
    .extrude(thickness + tube_length)
    .faces(">Z")
    .workplane()
    .circle(tube_inner / 2)
    .cutBlind(tube_length + thickness)
)

result = plate.union(tube)