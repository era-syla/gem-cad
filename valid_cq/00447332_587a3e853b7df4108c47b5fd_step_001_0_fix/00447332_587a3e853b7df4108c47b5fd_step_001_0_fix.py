import cadquery as cq
import math

# Parameters
R1 = 10   # radius of small pulley
R2 = 30   # radius of large pulley
D = 80    # distance between pulley centers
thickness = 5  # extrusion thickness

# Compute tangent angle
alpha = math.acos((R2 - R1) / D)

# Compute tangent points on small pulley
p1_small = (R1 * math.cos(alpha),  R1 * math.sin(alpha))
p2_small = (R1 * math.cos(alpha), -R1 * math.sin(alpha))

# Compute tangent points on large pulley
p1_big = (D + R2 * math.cos(alpha),  R2 * math.sin(alpha))
p2_big = (D + R2 * math.cos(alpha), -R2 * math.sin(alpha))

# Build the belt profile and extrude
belt = (
    cq.Workplane("XY")
    .moveTo(*p1_small)
    .lineTo(*p1_big)
    .threePointArc((D - R2, 0), p2_big)
    .lineTo(*p2_small)
    .threePointArc((-R1, 0), p1_small)
    .close()
    .extrude(thickness)
)

# Create the pulleys
pulley1 = cq.Workplane("XY").center(0, 0).circle(R1).extrude(thickness)
pulley2 = cq.Workplane("XY").center(D, 0).circle(R2).extrude(thickness)

# Combine into final result
result = belt.union(pulley1).union(pulley2)