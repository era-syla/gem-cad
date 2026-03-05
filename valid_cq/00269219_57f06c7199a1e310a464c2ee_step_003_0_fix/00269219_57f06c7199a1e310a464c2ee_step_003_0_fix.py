import cadquery as cq
import math

# Parameters
width = 20.0
thickness = 5.0
bottom_len = 40.0
beam_len = 100.0
top_len = 40.0
angle_deg = 30.0
angle = math.radians(angle_deg)

# Derived values
dx = beam_len * math.cos(angle)
dz = beam_len * math.sin(angle)

# Main bracket profile in XZ, extruded in Y
pts = [
    (0, 0),
    (bottom_len, 0),
    (bottom_len, thickness),
    (bottom_len + dx, thickness + dz),
    (bottom_len + dx, thickness + dz + thickness),
    (bottom_len + dx + top_len, thickness + dz + thickness),
    (bottom_len + dx + top_len, thickness + dz),
    (0, thickness),
]
result = cq.Workplane("XZ").polyline(pts).close().extrude(width)

# Gusset support
gfrac = 0.3
base1 = (bottom_len, thickness)
base2 = (bottom_len + dx * gfrac, thickness)
peak = (bottom_len + dx * gfrac, thickness + dz * gfrac)
gusset = cq.Workplane("XZ").polyline([base1, base2, peak]).close().extrude(width)
result = result.union(gusset)

# Holes
hole_radius = 3.0

# Bottom plate hole
bottom_hole = (
    cq.Workplane("XZ")
    .pushPoints([(bottom_len / 2.0, thickness / 2.0)])
    .circle(hole_radius)
    .extrude(width)
)
# Top plate hole
x_top = bottom_len + dx + top_len / 2.0
z_top = thickness + dz + thickness / 2.0
top_hole = (
    cq.Workplane("XZ")
    .pushPoints([(x_top, z_top)])
    .circle(hole_radius)
    .extrude(width)
)

result = result.cut(bottom_hole).cut(top_hole)