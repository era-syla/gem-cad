import cadquery as cq
import math

# Parametric dimensions
r_in = 50.0
r_out = 80.0
leg_length = 60.0
thickness = 12.0
hole_dia = 10.0
hole_dist_from_bottom = 15.0

bolt_radius = (r_in + r_out) / 2.0

# Create the main U-shaped body
base = (
    cq.Workplane("XY")
    .moveTo(r_out, -leg_length)
    .lineTo(r_out, 0)
    .threePointArc((0, r_out), (-r_out, 0))
    .lineTo(-r_out, -leg_length)
    .lineTo(-r_in, -leg_length)
    .lineTo(-r_in, 0)
    .threePointArc((0, r_in), (r_in, 0))
    .lineTo(r_in, -leg_length)
    .close()
    .extrude(thickness)
)

# Calculate hole positions
pts = []

# Holes on the semi-circular arc (30, 60, 90, 120, 150 degrees)
for angle_deg in range(30, 180, 30):
    angle_rad = math.radians(angle_deg)
    x = bolt_radius * math.cos(angle_rad)
    y = bolt_radius * math.sin(angle_rad)
    pts.append((x, y))

# Holes on the straight legs
pts.append((bolt_radius, -leg_length + hole_dist_from_bottom))
pts.append((-bolt_radius, -leg_length + hole_dist_from_bottom))

# Apply holes to the base geometry
result = (
    base.faces(">Z").workplane()
    .pushPoints(pts)
    .circle(hole_dia / 2.0)
    .cutThruAll()
)