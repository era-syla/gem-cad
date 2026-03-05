import cadquery as cq
import math

# Parameters
R_out = 100.0          # Outer radius of the arc
R_in = 65.0            # Inner radius of the arc
thickness = 15.0       # Extrusion thickness
leg_length = 80.0      # Length of the straight legs below the arc center
hole_radius = 5.0      # Radius of the holes
R_pitch = (R_out + R_in) / 2.0  # Pitch radius for holes

# Create the base U-shape profile
base = (cq.Workplane("XY")
    .moveTo(-R_out, -leg_length)
    .lineTo(-R_out, 0)
    .threePointArc((0, R_out), (R_out, 0))
    .lineTo(R_out, -leg_length)
    .lineTo(R_in, -leg_length)
    .lineTo(R_in, 0)
    .threePointArc((0, R_in), (-R_in, 0))
    .lineTo(-R_in, -leg_length)
    .close()
    .extrude(thickness)
)

# Calculate hole positions
hole_pts = []

# Leg holes (placed near the bottom of each leg)
leg_hole_y = -leg_length + (R_out - R_in) / 2.0
hole_pts.append((-R_pitch, leg_hole_y))
hole_pts.append((R_pitch, leg_hole_y))

# Arc holes (4 holes evenly distributed along the semi-circle)
angles_deg = [22.5, 67.5, 112.5, 157.5]
for angle in angles_deg:
    rad = math.radians(angle)
    x = R_pitch * math.cos(rad)
    y = R_pitch * math.sin(rad)
    hole_pts.append((x, y))

# Apply the holes to the geometry
result = (base.faces(">Z")
    .workplane()
    .pushPoints(hole_pts)
    .hole(hole_radius * 2.0)
)