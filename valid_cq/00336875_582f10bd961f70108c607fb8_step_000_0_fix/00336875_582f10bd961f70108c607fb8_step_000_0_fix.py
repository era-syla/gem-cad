import cadquery as cq
import math

# Parameters
d1 = 20    # length of bottom segment
d2 = 60    # length of vertical segment
d3 = 20    # length of top segment
w  = 10    # plate width in XY-plane
t  = 4     # plate thickness in Z
hole_d = 5 # hole diameter
offset_top = 12  # offset of the upper vertical hole from the bend
angle = 30       # angle of top segment from vertical

# Compute key points
P2 = (d1, d2)
rad = math.radians(angle)
dx3 = d3 * math.sin(rad)
dy3 = d3 * math.cos(rad)
P3 = (d1 + dx3, d2 + dy3)

# Create bottom horizontal box
bottom = cq.Workplane("XY") \
    .box(d1, w, t) \
    .translate((d1/2, 0, t/2))

# Create vertical box
vertical = cq.Workplane("XY") \
    .box(w, d2, t) \
    .translate((d1, d2/2, t/2))

# Create top slanted box
theta = math.degrees(math.atan2(dy3, dx3))
top = cq.Workplane("XY") \
    .box(d3, w, t) \
    .rotate((0, 0, 0), (0, 0, 1), theta)
cx = P2[0] + 0.5 * d3 * math.cos(math.radians(theta))
cy = P2[1] + 0.5 * d3 * math.sin(math.radians(theta))
top = top.translate((cx, cy, t/2))

# Combine all segments
result = bottom.union(vertical).union(top)

# Drill holes through the plate
hole_positions = [
    (0,         0),
    (d1,        d2/2),
    (d1,        d2 - offset_top),
    (P3[0],     P3[1])
]
result = result.faces(">Z").workplane().pushPoints(hole_positions).hole(hole_d)