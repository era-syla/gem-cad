import cadquery as cq

# Parameters
front = 30
ramp = 20
top_flat = 30
width = 20
t_base = 10
t_top = 10

# Create main body profile and extrude
pts = [
    (0, 0),
    (front, 0),
    (front, t_base),
    (front + ramp, t_base + t_top),
    (front + ramp + top_flat, t_base + t_top),
    (front + ramp + top_flat, 0)
]
result = cq.Workplane("XZ").polyline(pts).close().extrude(width)

# Fillet all edges slightly
result = result.edges().fillet(2)

# Top countersunk holes
pos1 = front + ramp + top_flat / 3
pos2 = front + ramp + 2 * top_flat / 3
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(pos1, 0), (pos2, 0)])
    .cskHole(6, 12, 90)
)

# Side through hole
result = result.faces(">X").workplane().hole(8)

# Add cylindrical boss on side
cyl_offset = -t_base/2 + 2
result = (
    result
    .faces(">X")
    .workplane()
    .center(0, cyl_offset)
    .circle(6)
    .extrude(-5)
)

# Add hexagonal boss on side
hex_offset = -t_base/2 - 4
result = (
    result
    .faces(">X")
    .workplane()
    .center(0, hex_offset)
    .polygon(6, 8)
    .extrude(-5)
)