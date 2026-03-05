import cadquery as cq
import math

# Parameters
n_turns = 8
pitch = 2.0
radius = 10.0
wire_radius = 1.5
coil_height = pitch * n_turns
steps = 200

# Generate helix path points
helix_pts = []
for i in range(steps + 1):
    t = i / steps
    angle = 2 * math.pi * n_turns * t
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    z = coil_height * t
    helix_pts.append((x, y, z))

# Create a spline wire for the helix
pathWire = cq.Workplane("XY").spline(helix_pts).val()

# Sweep a circle along the helix to make the coil
coil = cq.Workplane("XY") \
    .moveTo(radius, 0) \
    .circle(wire_radius) \
    .sweep(pathWire, isFrenet=True)

# Compute tangent at start for rod orientation
# At t=0: sin(0)=0, cos(0)=1
tangent = cq.Vector(0, radius * 2 * math.pi * n_turns, coil_height)
tangent_normalized = tangent.normalized()
z_axis = cq.Vector(0, 0, 1)
rot_axis = z_axis.cross(tangent_normalized)
rot_angle = math.degrees(math.acos(z_axis.dot(tangent_normalized)))

# Create entry rod (extends backward from start)
rod_length = 20.0
rod1 = cq.Workplane("XY") \
    .circle(wire_radius) \
    .extrude(-rod_length) \
    .rotate((0, 0, 0), rot_axis.toTuple(), rot_angle) \
    .translate(helix_pts[0])

# Create exit rod (extends forward from end)
rod2 = cq.Workplane("XY") \
    .circle(wire_radius) \
    .extrude(rod_length) \
    .rotate((0, 0, 0), rot_axis.toTuple(), rot_angle) \
    .translate(helix_pts[-1])

# Combine coil and rods
result = coil.union(rod1).union(rod2)