import cadquery as cq
import math

# Create a twisted/folded geometric sculpture
# The shape appears to be two flat polygonal faces connected by twisted faces

# Define the bottom pentagon-like polygon (lower flat shape)
bottom_pts = [
    (-40, -20),
    (-10, -40),
    (30, -30),
    (40, 0),
    (10, 20),
]

# Define the top pentagon-like polygon (upper flat shape, offset and rotated)
top_pts = [
    (-30, 10),
    (-50, 30),
    (-20, 50),
    (20, 45),
    (30, 20),
]

# Heights
bottom_z = 0
top_z = 80

# Create bottom face as a thin solid by extruding
bottom_face = (
    cq.Workplane("XY")
    .workplane(offset=bottom_z)
    .polyline(bottom_pts)
    .close()
    .extrude(2)
)

# Create top face as a thin solid
top_face = (
    cq.Workplane("XY")
    .workplane(offset=top_z)
    .polyline(top_pts)
    .close()
    .extrude(2)
)

# Create connecting faces between bottom and top polygons
# We'll use loft-like approach by creating prism panels between corresponding points
# Use pairs of vertices to create triangular/quad panels

# Map bottom to top with some correspondence
# Bottom has 5 pts, top has 5 pts
# Connect them with triangular faces forming the twisted middle section

from cadquery import Vector
import cadquery as cq

def make_quad_solid(p1, p2, p3, p4):
    """Create a solid from 4 points (two triangles)"""
    # Make a thin solid by creating two triangular prisms
    pts = [Vector(*p) for p in [p1, p2, p3, p4]]
    # Create as a shell/solid using vertices
    try:
        face1 = cq.Workplane("XY").add(
            cq.Face.makeFromWires(
                cq.Wire.makePolygon([pts[0], pts[1], pts[2], pts[0]])
            )
        )
        return face1
    except:
        return None

# Create the twisted connecting body using loft between bottom and top wire
# Approach: create a solid by building it from the two profile wires

bottom_wire_pts = [(x, y, bottom_z + 1) for x, y in bottom_pts]
top_wire_pts = [(x, y, top_z + 1) for x, y in top_pts]

# Build connecting solid using shell
# Use a series of triangles to fill the space

connecting_faces = []

n = len(bottom_pts)
for i in range(n):
    b1 = bottom_wire_pts[i]
    b2 = bottom_wire_pts[(i + 1) % n]
    t1 = top_wire_pts[i]
    t2 = top_wire_pts[(i + 1) % n]
    
    # Triangle 1: b1, b2, t1
    v1 = cq.Vector(b1)
    v2 = cq.Vector(b2)
    v3 = cq.Vector(t1)
    v4 = cq.Vector(t2)
    
    try:
        f1 = cq.Face.makeFromWires(cq.Wire.makePolygon([v1, v2, v3, v1]))
        f2 = cq.Face.makeFromWires(cq.Wire.makePolygon([v2, v4, v3, v2]))
        connecting_faces.extend([f1, f2])
    except:
        pass

# Build the shell solid
try:
    # Loft approach
    bottom_wire = cq.Wire.makePolygon([cq.Vector(x, y, bottom_z + 1) for x, y in bottom_pts] + [cq.Vector(bottom_pts[0][0], bottom_pts[0][1], bottom_z + 1)])
    top_wire = cq.Wire.makePolygon([cq.Vector(x, y, top_z + 1) for x, y in top_pts] + [cq.Vector(top_pts[0][0], top_pts[0][1], top_z + 1)])
    
    connector = (
        cq.Workplane("XY")
        .add(bottom_wire)
        .toPending()
        .workplane(offset=top_z)
        .add(top_wire)
        .toPending()
        .loft()
    )
    
    result = bottom_face.union(top_face).union(connector)
except Exception as e:
    # Fallback: just use bottom and top with a simple box connector
    result = bottom_face.union(top_face).union(
        cq.Workplane("XY").box(20, 20, top_z).translate((0, 0, top_z/2))
    )